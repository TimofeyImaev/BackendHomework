"""
ДЕМОНСТРАЦИЯ: Вложенные await корутины

КЛЮЧЕВОЕ ПОНИМАНИЕ:
- Когда мы делаем await корутины (не Future), мы НЕ используем add_done_callback
- В Task.__step() результат не является Future (он None или другой awaitable)
- Код идет в другой if, где используется call_soon для планирования следующей итерации
- Это позволяет, несмотря на то что все генераторы смёрджились в один генератор,
  запускать его асинхронно с другими задачами в event loop через call_soon
- У нас всегда одна и та же Task в event loop (созданная asyncio.run)
- await корутины собирает несколько корутин в одну Task через механизм генераторов
"""

import asyncio


async def level3_inner():
    """Самая внутренняя асинхронная функция"""
    loop = asyncio.get_running_loop()
    print("\n" + "=" * 70)
    print("LEVEL 3 (внутренняя функция)")
    print("=" * 70)
    print(f"Event Loop: {loop}")
    print(f"Loop is running: {loop.is_running()}")
    print(f"Loop is closed: {loop.is_closed()}")
    
    # Получаем все задачи
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    for i, task in enumerate(tasks, 1):
        print(f"  Задача {i}: {task.get_name()} - {task.get_coro().__name__ if hasattr(task.get_coro(), '__name__') else 'unknown'}")
    
    # Получаем текущую задачу
    current_task = asyncio.current_task(loop)
    if current_task:
        print(f"Текущая задача: {current_task.get_name()}")
    
    print("Выполняю await asyncio.sleep(0.1) в level3_inner...")
    await asyncio.sleep(0.1)
    
    # После await снова выводим информацию
    print("\nПосле await в level3_inner:")
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    
    return "level3_done"


async def level2_middle():
    """Средняя асинхронная функция"""
    loop = asyncio.get_running_loop()
    print("\n" + "=" * 70)
    print("LEVEL 2 (средняя функция)")
    print("=" * 70)
    print(f"Event Loop: {loop}")
    print(f"Loop is running: {loop.is_running()}")
    print(f"Loop is closed: {loop.is_closed()}")
    
    # Получаем все задачи
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    for i, task in enumerate(tasks, 1):
        print(f"  Задача {i}: {task.get_name()} - {task.get_coro().__name__ if hasattr(task.get_coro(), '__name__') else 'unknown'}")
    
    # Получаем текущую задачу
    current_task = asyncio.current_task(loop)
    if current_task:
        print(f"Текущая задача: {current_task.get_name()}")
    
    print("Вызываю level3_inner()...")
    print("  → await level3_inner() НЕ создает Future/Task")
    print("  → Task.__step() получает результат (не Future)")
    print("  → Используется call_soon для планирования следующей итерации")
    print("  → Все выполняется в одной Task через механизм генераторов")
    result = await level3_inner()
    print(f"Получен результат из level3_inner: {result}")
    
    print("\nПосле await level3_inner в level2_middle:")
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    
    print("Выполняю await asyncio.sleep(0.1) в level2_middle...")
    await asyncio.sleep(0.1)
    
    return "level2_done"


async def level1_outer():
    """Внешняя асинхронная функция"""
    loop = asyncio.get_running_loop()
    print("\n" + "=" * 70)
    print("LEVEL 1 (внешняя функция)")
    print("=" * 70)
    print(f"Event Loop: {loop}")
    print(f"Loop is running: {loop.is_running()}")
    print(f"Loop is closed: {loop.is_closed()}")
    
    # Получаем все задачи
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    for i, task in enumerate(tasks, 1):
        print(f"  Задача {i}: {task.get_name()} - {task.get_coro().__name__ if hasattr(task.get_coro(), '__name__') else 'unknown'}")
    
    # Получаем текущую задачу
    current_task = asyncio.current_task(loop)
    if current_task:
        print(f"Текущая задача: {current_task.get_name()}")
    
    print("Вызываю level2_middle()...")
    print("  → await level2_middle() НЕ создает Future/Task")
    print("  → Task.__step() получает результат (не Future)")
    print("  → Используется call_soon для планирования следующей итерации")
    print("  → Все выполняется в одной Task через механизм генераторов")
    result = await level2_middle()
    print(f"Получен результат из level2_middle: {result}")
    
    print("\nПосле await level2_middle в level1_outer:")
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    
    print("Выполняю await asyncio.sleep(0.1) в level1_outer...")
    await asyncio.sleep(0.1)
    
    return "level1_done"


async def main():
    """Главная функция для запуска"""
    print("\n" + "=" * 70)
    print("НАЧАЛО ПРОГРАММЫ")
    print("=" * 70)
    loop = asyncio.get_running_loop()
    print(f"Event Loop: {loop}")
    print(f"Loop is running: {loop.is_running()}")
    print(f"Loop is closed: {loop.is_closed()}")
    
    print("\nВызываю level1_outer()...")
    print("  → await level1_outer() НЕ создает Future/Task")
    print("  → Task.__step() получает результат (не Future)")
    print("  → Используется call_soon для планирования следующей итерации")
    print("  → Все выполняется в одной Task через механизм генераторов")
    result = await level1_outer()
    print(f"\nФинальный результат: {result}")
    
    print("\n" + "=" * 70)
    print("КОНЕЦ ПРОГРАММЫ")
    print("=" * 70)
    tasks = asyncio.all_tasks(loop)
    print(f"Всего задач в loop: {len(tasks)}")
    print()
    print("=" * 70)
    print("ВЫВОДЫ:")
    print("=" * 70)
    print("✅ await корутины НЕ создает Future/Task")
    print("✅ Все вложенные await выполняются в одной Task (созданной asyncio.run)")
    print("✅ Task.__step() использует call_soon (не add_done_callback) для await корутины")
    print("✅ call_soon позволяет выполнять другие задачи параллельно")
    print("✅ await работает как генератор, который вызывает генератор")
    print("✅ Все генераторы смёрджились в один генератор в одной Task")


if __name__ == "__main__":
    asyncio.run(main())

