"""
ВОПРОС: await делает последовательное выполнение?

Вы правы! await НЕ создает Task автоматически.
await работает ПОСЛЕДОВАТЕЛЬНО, но использует Future для приостановки.
"""

import asyncio
import time

# ============================================
# ТЕСТ 1: await - последовательное выполнение
# ============================================
print("=" * 70)
print("ТЕСТ 1: await - последовательное выполнение")
print("=" * 70)
print()

async def task1():
    print(f"[{time.time():.2f}] task1: начал")
    await asyncio.sleep(1)  # Ждем 1 сек
    print(f"[{time.time():.2f}] task1: завершил")
    return 1

async def task2():
    print(f"[{time.time():.2f}] task2: начал")
    await asyncio.sleep(0.5)  # Ждем 0.5 сек
    print(f"[{time.time():.2f}] task2: завершил")
    return 2

async def sequential():
    """await делает последовательное выполнение"""
    print("=== Последовательное выполнение через await ===")
    start = time.time()
    
    # await НЕ создает Task!
    # Корутины выполняются ПОСЛЕДОВАТЕЛЬНО
    result1 = await task1()  # Ждем завершения
    result2 = await task2()  # Только потом начинаем
    
    elapsed = time.time() - start
    print(f"Результаты: [{result1}, {result2}]")
    print(f"Время: {elapsed:.2f} сек (последовательно!)")
    print()

# ============================================
# ТЕСТ 2: create_task - параллельное выполнение
# ============================================
async def parallel():
    """create_task создает Task для параллельного выполнения"""
    print("=== Параллельное выполнение через create_task ===")
    start = time.time()
    
    # create_task СОЗДАЕТ Task!
    # Корутины выполняются ПАРАЛЛЕЛЬНО
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    
    result1 = await t1
    result2 = await t2
    
    elapsed = time.time() - start
    print(f"Результаты: [{result1}, {result2}]")
    print(f"Время: {elapsed:.2f} сек (параллельно!)")
    print()

# ============================================
# ТЕСТ 3: await НЕ создает Task
# ============================================
print("=" * 70)
print("ТЕСТ 3: await НЕ создает Task")
print("=" * 70)
print()

# Счетчик создания Task
task_count = 0
original_create_task = asyncio.create_task

def traced_create_task(coro, name=None):
    global task_count
    task_count += 1
    print(f"📦 Task #{task_count} создан: {coro}")
    return original_create_task(coro, name=name)

asyncio.create_task = traced_create_task

async def test_no_task_creation():
    """Показываем, что await НЕ создает Task"""
    print("Вызываем await task1() и await task2()")
    print("Ожидание: Task НЕ создастся (await не создает Task)")
    print()
    
    result1 = await task1()
    result2 = await task2()
    
    print(f"Результаты: [{result1}, {result2}]")
    print(f"Всего создано Task: {task_count}")

print("Запускаем тест:")
asyncio.run(test_no_task_creation())
print()

# ============================================
# ТЕСТ 4: await использует Future, но не создает Task
# ============================================
print("=" * 70)
print("ТЕСТ 4: await использует Future, но не создает Task")
print("=" * 70)
print()

print("Когда мы делаем: await asyncio.sleep(1)")
print()
print("1. asyncio.sleep(1) возвращает корутину")
print("2. await вызывает sleep_coro.__await__()")
print("3. __await__() возвращает Future (созданный внутри sleep)")
print("4. Task.__step() получает Future")
print("5. Task ждет Future через callback")
print()
print("→ await НЕ создает Task!")
print("→ await использует Future для приостановки")
print("→ Future создается ВНУТРИ корутины (например, в asyncio.sleep())")
print()

# ============================================
# ВЫВОД
# ============================================
print("=" * 70)
print("ВЫВОД")
print("=" * 70)
print()

print("✅ await делает ПОСЛЕДОВАТЕЛЬНОЕ выполнение")
print("   - await coro() НЕ создает Task")
print("   - Корутины выполняются одна за другой")
print()
print("✅ await использует Future для приостановки")
print("   - Future создается ВНУТРИ корутины")
print("   - await ждет Future через callback")
print("   - Event loop управляет приостановкой")
print()
print("✅ Task создается ТОЛЬКО через create_task()")
print("   - create_task() создает Task для параллельного выполнения")
print("   - await сам по себе НЕ создает Task")
print()
print("🔑 КЛЮЧЕВОЕ ПОНИМАНИЕ:")
print("   await = последовательное выполнение + Future для приостановки")
print("   create_task = создание Task для параллельного выполнения")































