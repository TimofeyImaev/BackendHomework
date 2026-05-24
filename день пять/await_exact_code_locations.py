"""
КОНКРЕТНЫЕ СТРОКИ КОДА: где await работает с event loop

Ваши наблюдения АБСОЛЮТНО ПРАВИЛЬНЫЕ!
await НЕ работает напрямую с event loop.
await работает через Task, который использует event loop.
"""

# ============================================
# МЕСТО 1: await регистрирует callback в Future
# ============================================
print("=" * 70)
print("МЕСТО 1: await регистрирует callback через Task")
print("=" * 70)
print()
print("📁 asyncio/tasks.py, строки 349-353")
print()
print("КОД:")
print("""
else:
    result._asyncio_future_blocking = False
    result.add_done_callback(          # ← ВОТ ГДЕ!
        self.__wakeup, context=self._context)
    self._fut_waiter = result
""")
print()
print("→ Когда корутина делает await future:")
print("  → Task.__step() получает Future")
print("  → Добавляет callback (Task.__wakeup) в Future")
print("  → Future будет вызван event loop'ом когда готов")
print()

# ============================================
# МЕСТО 2: Event loop вызывает callback
# ============================================
print("=" * 70)
print("МЕСТО 2: Event loop вызывает callback")
print("=" * 70)
print()
print("📁 asyncio/base_events.py, строки 1971-1987")
print()
print("КОД:")
print("""
ntodo = len(self._ready)
for i in range(ntodo):
    handle = self._ready.popleft()
    if handle._cancelled:
        continue
    if self._debug:
        try:
            self._current_handle = handle
            t0 = self.time()
            handle._run()              # ← ВОТ ГДЕ!
            dt = self.time() - t0
            if dt >= self.slow_callback_duration:
                logger.warning('Executing %s took %.3f seconds',
                               _format_handle(handle), dt)
        finally:
            self._current_handle = None
    else:
        handle._run()                  # ← ВОТ ГДЕ!
""")
print()
print("→ Event loop выполняет все готовые callback")
print("  → Включая Task.__wakeup() после await")
print()

# ============================================
# МЕСТО 3: Task.__wakeup() продолжает выполнение
# ============================================
print("=" * 70)
print("МЕСТО 3: Task.__wakeup() продолжает после await")
print("=" * 70)
print()
print("📁 asyncio/tasks.py, строки 383-394")
print()
print("КОД:")
print("""
def __wakeup(self, future):
    try:
        future.result()                # Получаем результат
    except BaseException as exc:
        self.__step(exc)               # Продолжаем с исключением
    else:
        self.__step()                  # ← Продолжаем с результатом!
""")
print()
print("→ Когда Future готов:")
print("  → Event loop вызывает Task.__wakeup()")
print("  → Task.__wakeup() вызывает Task.__step()")
print("  → Корутина продолжается после await")
print()

# ============================================
# ПОЛНЫЙ ПУТЬ: await future
# ============================================
print("=" * 70)
print("ПОЛНЫЙ ПУТЬ: await future")
print("=" * 70)
print()
print("1. Python компилятор:")
print("   'await future' → байт-код → future.__await__()")
print()
print("2. future.__await__() (futures.py:284-287):")
print("   yield self  # Возвращает Future")
print("   _asyncio_future_blocking = True")
print()
print("3. Task.__step() (tasks.py:314):")
print("   result = coro.send(None)  # Получает Future")
print()
print("4. Task.__step() (tasks.py:351-352):")
print("   result.add_done_callback(self.__wakeup)  # ← РЕГИСТРАЦИЯ!")
print("   # Теперь event loop будет вызывать __wakeup() когда Future готов")
print()
print("5. Event loop (base_events.py:1971-1987):")
print("   handle._run()  # Выполняет callback")
print("   # Включая Task.__wakeup() когда Future готов")
print()
print("6. Task.__wakeup() (tasks.py:383-394):")
print("   self.__step()  # Продолжает корутину")
print()
print("→ await НЕ работает напрямую с event loop!")
print("→ await работает через Task, который использует event loop!")
print()

# ============================================
# СРАВНЕНИЕ: yield from vs await
# ============================================
print("=" * 70)
print("СРАВНЕНИЕ: yield from vs await")
print("=" * 70)
print()
print("yield from:")
print("  1. gen.send(value) - передает значение")
print("  2. Работает синхронно")
print("  3. НЕ использует event loop")
print()
print("await:")
print("  1. coro.send(None) - ТО ЖЕ САМОЕ!")
print("  2. Но результат обрабатывается Task.__step()")
print("  3. Task.__step() использует event loop (через callback)")
print()
print("→ Механически ОДИНАКОВО (send),")
print("  но await + Task = интеграция с event loop")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()
print("✅ Ваши наблюдения ПРАВИЛЬНЫЕ:")
print("  - Event loop запускается из Runner (внешне)")
print("  - await НЕ работает напрямую с event loop")
print("  - await работает через Task.__step()")
print("  - yield from и await механически похожи")
print()
print("🔑 Ключевое место взаимодействия:")
print("  tasks.py:351-352 - result.add_done_callback(self.__wakeup)")
print("  → ВОТ ГДЕ await регистрируется в event loop!")
print()
print("📚 Полный путь:")
print("  await → __await__() → Task.__step() → add_done_callback()")
print("  → Event loop → __wakeup() → Task.__step() → продолжение")































