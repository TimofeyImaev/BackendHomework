"""
ПРАКТИЧЕСКАЯ ДЕМОНСТРАЦИЯ: await vs yield from

Ключевое различие: await возвращает управление в event loop,
yield from - НЕТ!
"""

import asyncio
import time
from types import coroutine as types_coroutine

# ============================================
# ДЕМОНСТРАЦИЯ: await возвращает управление в loop
# ============================================

async def task_a():
    print(f"[{time.time():.2f}] task_a: начал")
    await asyncio.sleep(1)  # ← await возвращает управление в loop!
    print(f"[{time.time():.2f}] task_a: завершил")
    return "A"

async def task_b():
    print(f"[{time.time():.2f}] task_b: начал")
    await asyncio.sleep(0.5)  # ← await возвращает управление в loop!
    print(f"[{time.time():.2f}] task_b: завершил")
    return "B"

async def main_with_await():
    """await позволяет параллельное выполнение"""
    print("\n=== await: параллельное выполнение ===")
    start = time.time()
    
    # Обе корутины выполняются ПАРАЛЛЕЛЬНО!
    results = await asyncio.gather(task_a(), task_b())
    
    elapsed = time.time() - start
    print(f"Результаты: {results}")
    print(f"Время выполнения: {elapsed:.2f} сек (параллельно!)")
    print()

# ============================================
# ДЕМОНСТРАЦИЯ: yield from НЕ возвращает управление
# ============================================

@types_coroutine
def blocking_task_a():
    print(f"[{time.time():.2f}] blocking_task_a: начал")
    yield from asyncio.sleep(1)  # ← yield from НЕ возвращает управление!
    print(f"[{time.time():.2f}] blocking_task_a: завершил")
    return "A"

@types_coroutine
def blocking_task_b():
    print(f"[{time.time():.2f}] blocking_task_b: начал")
    yield from asyncio.sleep(0.5)  # ← yield from НЕ возвращает управление!
    print(f"[{time.time():.2f}] blocking_task_b: завершил")
    return "B"

@types_coroutine
def main_with_yield_from():
    """yield from блокирует выполнение"""
    print("=== yield from: последовательное выполнение ===")
    start = time.time()
    
    # Корутины выполняются ПОСЛЕДОВАТЕЛЬНО!
    result_a = yield from blocking_task_a()
    result_b = yield from blocking_task_b()
    
    elapsed = time.time() - start
    print(f"Результаты: [{result_a}, {result_b}]")
    print(f"Время выполнения: {elapsed:.2f} сек (последовательно!)")
    print()

# ============================================
# КЛЮЧЕВОЕ РАЗЛИЧИЕ: Event Loop
# ============================================

async def demonstrate_event_loop_integration():
    """Показываем интеграцию с event loop"""
    print("=== Как await работает с event loop ===")
    
    async def coro1():
        print("coro1: начал")
        await asyncio.sleep(0.1)  # ← Возвращает управление в loop
        print("coro1: продолжил")
        await asyncio.sleep(0.1)  # ← Снова возвращает управление
        print("coro1: завершил")
    
    async def coro2():
        print("coro2: начал")
        await asyncio.sleep(0.05)  # ← Может выполниться пока coro1 ждет!
        print("coro2: завершил")
    
    # Обе корутины выполняются "одновременно"
    await asyncio.gather(coro1(), coro2())
    print()

# ============================================
# ВНУТРЕННИЙ МЕХАНИЗМ
# ============================================

def explain_internal_mechanism():
    """Объясняем внутренний механизм"""
    print("=== Внутренний механизм ===")
    print()
    print("yield from:")
    print("  1. gen.send(value) передает значение")
    print("  2. Работает синхронно в текущем контексте")
    print("  3. НЕ возвращает управление в event loop")
    print("  4. Блокирует выполнение до завершения")
    print()
    print("await:")
    print("  1. coro.__await__() возвращает awaitable итератор")
    print("  2. Event loop управляет выполнением")
    print("  3. ВОЗВРАЩАЕТ управление в event loop")
    print("  4. Позволяет параллельное выполнение")
    print()
    print("await = yield from + интеграция с event loop")

# ============================================
# ЗАПУСК
# ============================================

if __name__ == "__main__":
    explain_internal_mechanism()
    
    # Тест с await
    asyncio.run(main_with_await())
    
    # Тест с yield from
    asyncio.run(asyncio.ensure_future(main_with_yield_from()))
    
    # Демонстрация event loop
    asyncio.run(demonstrate_event_loop_integration())
    
    print("=== ВЫВОД ===")
    print("await и yield from отличаются НЕ только типом!")
    print("Главное различие: await интегрирован с event loop,")
    print("yield from - нет. Поэтому await позволяет параллелизм,")
    print("а yield from - только последовательное выполнение.")




























