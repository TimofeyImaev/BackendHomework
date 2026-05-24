"""
ПОЛНЫЙ ПУТЬ: от C-кода await до event loop

Вы нашли ПРАВИЛЬНЫЙ код! Это именно то, что компилирует await.
"""

# ============================================
# 1. C-КОД: что вы нашли
# ============================================
print("=" * 70)
print("1. C-КОД: что вы нашли")
print("=" * 70)
print()
print("📁 ceval.c: _PyCoro_GetAwaitableIter()")
print("   → Вызывается когда Python видит 'await'")
print("   → Получает awaitable итератор через __await__()")
print()
print("📁 ceval.c: _PyEval_GetAwaitable()")
print("   → Проверяет, что объект awaitable")
print("   → Вызывает _PyCoro_GetAwaitableIter()")
print()
print("📁 genobject.c: coro_await()")
print("   → Создает PyCoroWrapper для корутины")
print("   → Это итератор, который используется await")
print()
print("→ Этот код компилирует 'await obj' в байт-код!")
print()

# ============================================
# 2. ПОЛНЫЙ ПУТЬ: от await до event loop
# ============================================
print("=" * 70)
print("2. ПОЛНЫЙ ПУТЬ: от await до event loop")
print("=" * 70)
print()
print("ШАГ 1: Python компилятор (compile.c)")
print("   'await future' → байт-код GET_AWAITABLE")
print()
print("ШАГ 2: Интерпретатор (ceval.c)")
print("   GET_AWAITABLE → _PyEval_GetAwaitable()")
print("   → _PyCoro_GetAwaitableIter()")
print("   → Вызывает obj.__await__()")
print()
print("ШАГ 3: Python-код (futures.py:284)")
print("   future.__await__() → yield self")
print("   → Возвращает Future (awaitable итератор)")
print()
print("ШАГ 4: Task.__step() (tasks.py:314)")
print("   result = coro.send(None)  # Получает Future")
print()
print("ШАГ 5: Task.__step() (tasks.py:351-352)")
print("   result.add_done_callback(self.__wakeup)")
print("   → РЕГИСТРАЦИЯ в event loop!")
print()
print("ШАГ 6: Event loop (base_events.py:1971-1987)")
print("   handle._run()  # Вызывает Task.__wakeup()")
print()
print("ШАГ 7: Task.__wakeup() (tasks.py:383-394)")
print("   self.__step()  # Продолжает корутину")
print()

# ============================================
# 3. ГДЕ ВЫЗЫВАЕТСЯ EVENT LOOP
# ============================================
print("=" * 70)
print("3. ГДЕ ВЫЗЫВАЕТСЯ EVENT LOOP")
print("=" * 70)
print()
print("📁 asyncio/runners.py, строка 118")
print("   return self._loop.run_until_complete(task)")
print("   → ВОТ ГДЕ запускается event loop!")
print()
print("📁 asyncio/base_events.py, строка 627-649")
print("   def run_forever(self):")
print("       while True:")
print("           self._run_once()  # ← Главный цикл!")
print("           if self._stopping:")
print("               break")
print()
print("📁 asyncio/base_events.py, строка 1910-1988")
print("   def _run_once(self):")
print("       # Обрабатывает готовые callback")
print("       # Включая Task.__wakeup() после await")
print()

# ============================================
# 4. ГДЕ ВЫЗЫВАЕТСЯ create_task
# ============================================
print("=" * 70)
print("4. ГДЕ ВЫЗЫВАЕТСЯ create_task")
print("=" * 70)
print()
print("📁 asyncio/runners.py, строка 100")
print("   task = self._loop.create_task(coro, context=context)")
print("   → Runner создает Task для главной корутины")
print()
print("📁 asyncio/tasks.py, строка 412-425")
print("   def create_task(coro, *, name=None, context=None):")
print("       loop = events.get_running_loop()")
print("       task = loop.create_task(coro)")
print("   → Публичный API для создания Task")
print()
print("📁 asyncio/base_events.py, строка 451-470")
print("   def create_task(self, coro, *, name=None, context=None):")
print("       task = tasks.Task(coro, loop=self, name=name)")
print("       return task")
print("   → Реализация в BaseEventLoop")
print()
print("📁 asyncio/tasks.py, строка 111-140")
print("   def __init__(self, coro, *, loop=None, name=None, ...):")
print("       self._loop.call_soon(self.__step, ...)")
print("   → Task создается и сразу планируется в event loop!")
print()

# ============================================
# 5. СВЯЗЬ: C-код → Python-код → Event loop
# ============================================
print("=" * 70)
print("5. СВЯЗЬ: C-код → Python-код → Event loop")
print("=" * 70)
print()
print("C-КОД (ceval.c):")
print("  await obj → _PyEval_GetAwaitable()")
print("  → Вызывает obj.__await__()")
print()
print("PYTHON-КОД (futures.py):")
print("  Future.__await__() → yield self")
print("  → Возвращает Future")
print()
print("PYTHON-КОД (tasks.py):")
print("  Task.__step() → получает Future")
print("  → result.add_done_callback(self.__wakeup)")
print("  → РЕГИСТРАЦИЯ в event loop!")
print()
print("PYTHON-КОД (base_events.py):")
print("  Event loop → вызывает callback")
print("  → Task.__wakeup() → Task.__step()")
print("  → Корутина продолжается!")
print()

# ============================================
# 6. ГДЕ ЕЩЕ ПОСМОТРЕТЬ
# ============================================
print("=" * 70)
print("6. ГДЕ ЕЩЕ ПОСМОТРЕТЬ")
print("=" * 70)
print()
print("📁 CPython исходники (C-код):")
print("   - ceval.c: _PyEval_GetAwaitable() - обработка await")
print("   - genobject.c: coro_await() - создание awaitable итератора")
print("   - compile.c: компиляция await в байт-код")
print()
print("📁 asyncio (Python-код):")
print("   - runners.py:100, 118 - запуск event loop")
print("   - tasks.py:111-140 - создание Task")
print("   - tasks.py:291-394 - Task.__step() и __wakeup()")
print("   - futures.py:284-290 - Future.__await__()")
print("   - base_events.py:627-649 - run_forever()")
print("   - base_events.py:1910-1988 - _run_once()")
print()

# ============================================
# 7. БАЙТ-КОД: что генерируется
# ============================================
print("=" * 70)
print("7. БАЙТ-КОД: что генерируется")
print("=" * 70)

import dis

async def example():
    await asyncio.sleep(1)
    return 42

print()
print("Байт-код для 'await asyncio.sleep(1)':")
print()
dis.dis(example)
print()
print("GET_AWAITABLE - это опкод, который вызывает")
print("_PyEval_GetAwaitable() в ceval.c!")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()
print("✅ Вы нашли ПРАВИЛЬНЫЙ код!")
print("   C-код в ceval.c - это то, что обрабатывает await")
print()
print("🔗 Полная цепочка:")
print("   1. C-код (ceval.c) → компилирует await")
print("   2. Python-код (futures.py) → __await__()")
print("   3. Python-код (tasks.py) → Task.__step()")
print("   4. Python-код (base_events.py) → event loop")
print()
print("📍 Где вызывается event loop:")
print("   runners.py:118 → loop.run_until_complete()")
print()
print("📍 Где вызывается create_task:")
print("   runners.py:100 → loop.create_task()")
print("   tasks.py:412 → create_task() (публичный API)")































