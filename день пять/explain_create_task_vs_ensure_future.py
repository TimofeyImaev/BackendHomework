"""
ОБЪЯСНЕНИЕ: Разница между create_task() и ensure_future()

1. create_task(coro):
   - Проверяет: coroutines.iscoroutine(coro) - строгая проверка
   - Работает ТОЛЬКО с нативными корутинами (async def)
   - НЕ работает с generator-based корутинами (@types.coroutine)
   - Выбрасывает TypeError, если не корутина

2. ensure_future(coro_or_future):
   - Проверяет: сначала iscoroutine(), потом isawaitable()
   - Работает с корутинами, Future, и awaitable объектами
   - Может обернуть generator-based корутину в async функцию
   - Более гибкий, но медленнее

ПРОБЛЕМА: В Python 3.8+ generator-based корутины (@types.coroutine)
могут не работать правильно с ensure_future() тоже!

РЕШЕНИЕ: Используйте async def + await (современный способ)
"""

import asyncio
from types import coroutine as types_coroutine
import inspect

@types_coroutine
def generator_based_coro():
    yield from asyncio.sleep(0.1)
    return 42

async def native_coro():
    await asyncio.sleep(0.1)
    return 42

# Проверяем типы
gen_coro = generator_based_coro()
native_coro_obj = native_coro()

print("=== ДИАГНОСТИКА ===")
print(f"generator_based_coro() тип: {type(gen_coro)}")
print(f"  isgenerator: {inspect.isgenerator(gen_coro)}")
print(f"  iscoroutine (asyncio): {asyncio.iscoroutine(gen_coro)}")
print(f"  isawaitable: {inspect.isawaitable(gen_coro)}")
print()

print(f"native_coro() тип: {type(native_coro_obj)}")
print(f"  isgenerator: {inspect.isgenerator(native_coro_obj)}")
print(f"  iscoroutine (asyncio): {asyncio.iscoroutine(native_coro_obj)}")
print(f"  isawaitable: {inspect.isawaitable(native_coro_obj)}")
print()

# Пробуем create_task
print("=== create_task() ===")
try:
    task1 = asyncio.create_task(native_coro_obj)
    print("✓ create_task(native_coro) работает")
except Exception as e:
    print(f"✗ create_task(native_coro) ошибка: {e}")

try:
    task2 = asyncio.create_task(gen_coro)
    print("✓ create_task(generator_coro) работает")
except Exception as e:
    print(f"✗ create_task(generator_coro) ошибка: {e}")
print()

# Пробуем ensure_future
print("=== ensure_future() ===")
try:
    task3 = asyncio.ensure_future(native_coro_obj)
    print("✓ ensure_future(native_coro) работает")
except Exception as e:
    print(f"✗ ensure_future(native_coro) ошибка: {e}")

try:
    task4 = asyncio.ensure_future(gen_coro)
    print("✓ ensure_future(generator_coro) работает")
except Exception as e:
    print(f"✗ ensure_future(generator_coro) ошибка: {e}")




















