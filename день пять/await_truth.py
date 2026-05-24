"""
ПРАВДА ОБ await: последовательное выполнение БЕЗ создания Task

Вы АБСОЛЮТНО ПРАВЫ!
await делает ПОСЛЕДОВАТЕЛЬНОЕ выполнение.
await НЕ создает Task.
Future создается ВНУТРИ корутин, а не await'ом.
"""

import asyncio
import time

# ============================================
# ПРАВДА 1: await - последовательное выполнение
# ============================================
print("=" * 70)
print("ПРАВДА 1: await - последовательное выполнение")
print("=" * 70)
print()

async def slow_task(name, delay):
    print(f"[{time.time():.2f}] {name}: начал")
    await asyncio.sleep(delay)
    print(f"[{time.time():.2f}] {name}: завершил")
    return name

async def sequential_await():
    """await делает последовательное выполнение"""
    print("=== await - последовательное выполнение ===")
    start = time.time()
    
    # await НЕ создает Task!
    # Корутины выполняются ПОСЛЕДОВАТЕЛЬНО
    result1 = await slow_task("task1", 1.0)  # Ждем 1 сек
    result2 = await slow_task("task2", 0.5)  # Потом еще 0.5 сек
    
    elapsed = time.time() - start
    print(f"Результаты: [{result1}, {result2}]")
    print(f"Время: {elapsed:.2f} сек (последовательно: 1.0 + 0.5 = 1.5)")
    print()

# ============================================
# ПРАВДА 2: await НЕ создает Task
# ============================================
print("=" * 70)
print("ПРАВДА 2: await НЕ создает Task")
print("=" * 70)
print()

task_count = 0
original_create_task = asyncio.create_task

def traced_create_task(coro, name=None):
    global task_count
    task_count += 1
    print(f"📦 Task #{task_count} создан: {coro}")
    return original_create_task(coro, name=name)

asyncio.create_task = traced_create_task

async def test_await_no_task():
    """Показываем, что await НЕ создает Task"""
    print("Вызываем await slow_task() дважды")
    print("Ожидание: Task НЕ создастся")
    print()
    
    result1 = await slow_task("task1", 0.1)
    result2 = await slow_task("task2", 0.1)
    
    print(f"Результаты: [{result1}, {result2}]")
    print(f"Всего создано Task: {task_count}")
    print("→ await НЕ создал ни одного Task!")
    print()

print("Запускаем тест:")
asyncio.run(test_await_no_task())
print()

# ============================================
# ПРАВДА 3: Future создается ВНУТРИ корутин
# ============================================
print("=" * 70)
print("ПРАВДА 3: Future создается ВНУТРИ корутин")
print("=" * 70)
print()

print("Когда мы делаем: await asyncio.sleep(1)")
print()
print("1. asyncio.sleep(1) ВНУТРИ создает Future")
print("   📁 tasks.py: sleep() → создает Future")
print()
print("2. await вызывает sleep_coro.__await__()")
print("   → Возвращает Future (уже созданный внутри sleep)")
print()
print("3. Task.__step() получает Future")
print("   → Ждет Future через callback")
print()
print("→ await НЕ создает Future!")
print("→ Future создается ВНУТРИ корутины (asyncio.sleep)")
print("→ await просто использует этот Future")
print()

# ============================================
# ПРАВДА 4: await использует Future для приостановки
# ============================================
print("=" * 70)
print("ПРАВДА 4: await использует Future для приостановки")
print("=" * 70)
print()

print("await работает так:")
print()
print("1. await coro() → вызывает coro.__await__()")
print("2. coro.__await__() → возвращает Future (созданный внутри coro)")
print("3. Task.__step() → получает Future")
print("4. Task.__step() → result.add_done_callback(self.__wakeup)")
print("5. Task приостанавливается")
print("6. Event loop продолжает выполнение других задач")
print("7. Когда Future готов → вызывает __wakeup()")
print("8. Task продолжается")
print()
print("→ await использует Future для ПРИОСТАНОВКИ")
print("→ Но Future создается ВНУТРИ корутины, не await'ом")
print()

# ============================================
# СРАВНЕНИЕ: await vs create_task
# ============================================
print("=" * 70)
print("СРАВНЕНИЕ: await vs create_task")
print("=" * 70)
print()

async def comparison():
    print("=== await - последовательное ===")
    start = time.time()
    r1 = await slow_task("A", 0.5)
    r2 = await slow_task("B", 0.5)
    elapsed1 = time.time() - start
    print(f"Время: {elapsed1:.2f} сек (последовательно)")
    print()
    
    print("=== create_task - параллельное ===")
    start = time.time()
    t1 = asyncio.create_task(slow_task("A", 0.5))
    t2 = asyncio.create_task(slow_task("B", 0.5))
    r1 = await t1
    r2 = await t2
    elapsed2 = time.time() - start
    print(f"Время: {elapsed2:.2f} сек (параллельно)")
    print()
    
    print(f"Разница: {elapsed1 - elapsed2:.2f} сек")
    print("→ create_task быстрее, потому что параллельно!")

asyncio.run(comparison())
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ await делает ПОСЛЕДОВАТЕЛЬНОЕ выполнение")
print("   - Корутины выполняются одна за другой")
print("   - Нет параллелизма")
print()
print("✅ await НЕ создает Task")
print("   - Task создается ТОЛЬКО через create_task()")
print("   - await сам по себе не создает Task")
print()
print("✅ Future создается ВНУТРИ корутин")
print("   - asyncio.sleep() создает Future внутри")
print("   - await просто использует этот Future")
print("   - await НЕ создает Future")
print()
print("✅ await использует Future для приостановки")
print("   - Future позволяет приостановить выполнение")
print("   - Event loop может выполнять другие задачи")
print("   - Но await сам по себе последовательный")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("   await = последовательное выполнение + Future для приостановки")
print("   create_task = создание Task для параллельного выполнения")
print()
print("📚 Когда использовать:")
print("   await - когда нужно ждать результат последовательно")
print("   create_task - когда нужно параллельное выполнение")































