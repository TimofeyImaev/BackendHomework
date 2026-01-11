import asyncio
import traceback

"""
ВОПРОС: Создает ли asyncio.gather() Task для каждой корутины?

ОТВЕТ: ДА! gather() использует ensure_future(), который создает Task.

Как это работает внутри (tasks.py строка 829-831):
    for arg in coros_or_futures:
        if arg not in arg_to_fut:
            fut = ensure_future(arg, loop=loop)  # ← Создает Task для корутины!
            
Для каждой корутины, переданной в gather():
1. Вызывается ensure_future(coro)
2. ensure_future() проверяет, это корутина или Future
3. Если корутина → создается Task через loop.create_task()
4. Task добавляется в список children
5. Все Task выполняются параллельно

ВАЖНО: gather() автоматически создает Task, поэтому вам НЕ нужно
делать create_task() вручную перед gather()!
"""

# Счетчик создания Task
task_creation_count = 0

# Сохраняем оригинальные функции
original_create_task = asyncio.create_task
original_ensure_future = asyncio.ensure_future

def traced_create_task(coro, name=None):
    """Отслеживание create_task()"""
    global task_creation_count
    task_creation_count += 1
    
    print(f"\n📦 Task #{task_creation_count} создан через create_task()")
    print(f"   Корутина: {coro}")
    
    stack = traceback.extract_stack()[:-1]
    if stack:
        caller = stack[-1]
        print(f"   Вызван из: {caller.filename.split('/')[-1]}:{caller.lineno} в {caller.name}()")
    
    return original_create_task(coro, name=name)

def traced_ensure_future(coro_or_future, loop=None):
    """Отслеживание ensure_future() - именно это использует gather()!"""
    global task_creation_count
    
    # Проверяем, это корутина или уже Future
    if asyncio.isfuture(coro_or_future):
        print(f"\n✓ ensure_future получил уже готовый Future: {coro_or_future}")
        return original_ensure_future(coro_or_future, loop=loop)
    
    # Это корутина - будет создан Task
    task_creation_count += 1
    print(f"\n📦 Task #{task_creation_count} создан через ensure_future()")
    print(f"   Корутина: {coro_or_future}")
    
    stack = traceback.extract_stack()[:-1]
    if stack:
        caller = stack[-1]
        print(f"   Вызван из: {caller.filename.split('/')[-1]}:{caller.lineno} в {caller.name}()")
    
    return original_ensure_future(coro_or_future, loop=loop)

# Подменяем функции
asyncio.create_task = traced_create_task
asyncio.ensure_future = traced_ensure_future

async def task1():
    print("task1: начал")
    await asyncio.sleep(1)
    print("task1: завершил")
    return 1

async def task2():
    print("task2: начал") 
    await asyncio.sleep(0.5)
    print("task2: завершил")
    return 2

async def main():
    print("\n=== Вызываем asyncio.gather(task1(), task2()) ===")
    print("Ожидание: gather() создаст Task для каждой корутины через ensure_future()")
    
    # gather() внутри вызывает ensure_future() для каждой корутины!
    results = await asyncio.gather(task1(), task2())
    
    print(f"\nРезультаты: {results}")
    print(f"\nВсего создано Task: {task_creation_count}")

print("=== Запускаем тест ===")
asyncio.run(main())