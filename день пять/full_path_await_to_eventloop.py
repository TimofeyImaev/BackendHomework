"""
ПОЛНЫЙ ПУТЬ: от C-кода await до event loop

Вы нашли ПРАВИЛЬНЫЙ код! Показываю полную цепочку.
"""

import asyncio
import dis

# ============================================
# ПОЛНАЯ ЦЕПОЧКА: от await до event loop
# ============================================
print("=" * 70)
print("ПОЛНАЯ ЦЕПОЧКА: от await до event loop")
print("=" * 70)
print()

print("1️⃣  КОМПИЛЯЦИЯ (compile.c)")
print("   'await future' → байт-код GET_AWAITABLE")
print()

print("2️⃣  ИНТЕРПРЕТАЦИЯ (ceval.c)")
print("   GET_AWAITABLE → _PyEval_GetAwaitable()")
print("   → _PyCoro_GetAwaitableIter()")
print("   → Вызывает obj.__await__()")
print("   📁 ceval.c: _PyEval_GetAwaitable()")
print()

print("3️⃣  PYTHON: __await__() (futures.py:284-290)")
print("   future.__await__() → yield self")
print("   → Возвращает Future (awaitable итератор)")
print("   📁 asyncio/futures.py, строка 284")
print()

print("4️⃣  PYTHON: Task.__step() (tasks.py:314)")
print("   result = coro.send(None)  # Получает Future")
print("   📁 asyncio/tasks.py, строка 314")
print()

print("5️⃣  PYTHON: Регистрация в event loop (tasks.py:351-352)")
print("   result.add_done_callback(self.__wakeup)")
print("   → ВОТ ГДЕ await регистрируется в event loop!")
print("   📁 asyncio/tasks.py, строка 351-352")
print()

print("6️⃣  PYTHON: Event loop запускается (runners.py:118)")
print("   loop.run_until_complete(task)")
print("   → ВОТ ГДЕ запускается event loop!")
print("   📁 asyncio/runners.py, строка 118")
print()

print("7️⃣  PYTHON: Главный цикл (base_events.py:627-649)")
print("   run_forever() → while True: _run_once()")
print("   📁 asyncio/base_events.py, строка 627")
print()

print("8️⃣  PYTHON: Обработка callback (base_events.py:1971-1987)")
print("   handle._run()  # Вызывает Task.__wakeup()")
print("   📁 asyncio/base_events.py, строка 1979, 1987")
print()

print("9️⃣  PYTHON: Продолжение корутины (tasks.py:383-394)")
print("   Task.__wakeup() → self.__step()")
print("   → Корутина продолжается после await!")
print("   📁 asyncio/tasks.py, строка 383-394")
print()

# ============================================
# КОНКРЕТНЫЕ МЕСТА: где вызывается event loop
# ============================================
print("=" * 70)
print("КОНКРЕТНЫЕ МЕСТА: где вызывается event loop")
print("=" * 70)
print()

print("📍 МЕСТО 1: Runner.run()")
print("   📁 asyncio/runners.py, строка 118")
print("   return self._loop.run_until_complete(task)")
print("   → ВОТ ГДЕ запускается event loop из asyncio.run()!")
print()

print("📍 МЕСТО 2: BaseEventLoop.run_until_complete()")
print("   📁 asyncio/base_events.py, строка 674")
print("   self.run_forever()")
print("   → Вызывает главный цикл")
print()

print("📍 МЕСТО 3: BaseEventLoop.run_forever()")
print("   📁 asyncio/base_events.py, строка 640-643")
print("   while True:")
print("       self._run_once()  # ← Главный цикл!")
print("       if self._stopping:")
print("           break")
print()

# ============================================
# КОНКРЕТНЫЕ МЕСТА: где вызывается create_task
# ============================================
print("=" * 70)
print("КОНКРЕТНЫЕ МЕСТА: где вызывается create_task")
print("=" * 70)
print()

print("📍 МЕСТО 1: Runner.run()")
print("   📁 asyncio/runners.py, строка 100")
print("   task = self._loop.create_task(coro, context=context)")
print("   → Runner создает Task для главной корутины")
print()

print("📍 МЕСТО 2: asyncio.create_task()")
print("   📁 asyncio/tasks.py, строка 412-425")
print("   def create_task(coro, *, name=None, context=None):")
print("       loop = events.get_running_loop()")
print("       task = loop.create_task(coro)")
print("   → Публичный API для создания Task")
print()

print("📍 МЕСТО 3: BaseEventLoop.create_task()")
print("   📁 asyncio/base_events.py, строка 451-470")
print("   def create_task(self, coro, *, name=None, context=None):")
print("       task = tasks.Task(coro, loop=self, name=name)")
print("       return task")
print("   → Реализация в BaseEventLoop")
print()

print("📍 МЕСТО 4: Task.__init__()")
print("   📁 asyncio/tasks.py, строка 139")
print("   self._loop.call_soon(self.__step, context=self._context)")
print("   → Task создается и сразу планируется в event loop!")
print()

# ============================================
# БАЙТ-КОД: что генерируется из await
# ============================================
print("=" * 70)
print("БАЙТ-КОД: что генерируется из await")
print("=" * 70)
print()

async def example():
    await asyncio.sleep(1)
    return 42

print("Код: await asyncio.sleep(1)")
print()
print("Байт-код:")
dis.dis(example)
print()
print("GET_AWAITABLE - это опкод, который вызывает")
print("_PyEval_GetAwaitable() в ceval.c!")
print()

# ============================================
# СВЯЗЬ: C-код → Python-код
# ============================================
print("=" * 70)
print("СВЯЗЬ: C-код → Python-код")
print("=" * 70)
print()

print("C-КОД (ceval.c):")
print("  _PyEval_GetAwaitable()")
print("  → Вызывает obj.__await__()")
print("  → Это тот код, который вы нашли!")
print()

print("↓")
print()

print("PYTHON-КОД (futures.py:284):")
print("  def __await__(self):")
print("      yield self")
print("  → Возвращает Future")
print()

print("↓")
print()

print("PYTHON-КОД (tasks.py:314, 351-352):")
print("  result = coro.send(None)  # Получает Future")
print("  result.add_done_callback(self.__wakeup)  # Регистрация!")
print()

print("↓")
print()

print("PYTHON-КОД (base_events.py:1979, 1987):")
print("  handle._run()  # Вызывает callback")
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
print("   1. C-код (ceval.c) → _PyEval_GetAwaitable()")
print("   2. Python-код (futures.py) → __await__()")
print("   3. Python-код (tasks.py) → Task.__step()")
print("   4. Python-код (tasks.py) → add_done_callback()")
print("   5. Python-код (runners.py) → run_until_complete()")
print("   6. Python-код (base_events.py) → run_forever()")
print("   7. Python-код (base_events.py) → _run_once()")
print("   8. Python-код (base_events.py) → handle._run()")
print("   9. Python-код (tasks.py) → Task.__wakeup()")
print()

print("📍 Где вызывается event loop:")
print("   runners.py:118 → loop.run_until_complete()")
print("   base_events.py:674 → loop.run_forever()")
print("   base_events.py:640 → while True: _run_once()")
print()

print("📍 Где вызывается create_task:")
print("   runners.py:100 → loop.create_task()")
print("   tasks.py:412 → create_task() (публичный API)")
print("   base_events.py:451 → create_task() (реализация)")
print("   tasks.py:139 → call_soon(__step) (планирование)")



























