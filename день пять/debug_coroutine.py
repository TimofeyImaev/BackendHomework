import asyncio
import sys

print(f"Python version: {sys.version}")

# Проверяем, есть ли asyncio.coroutine
if hasattr(asyncio, 'coroutine'):
    print("asyncio.coroutine доступен")
else:
    print("asyncio.coroutine НЕ доступен (удален в Python 3.8+)")

# Пробуем использовать types.coroutine
from types import coroutine as types_coroutine

@types_coroutine
def test_gen():
    print("test_gen вызван")
    result = yield from asyncio.sleep(0.1)
    print(f"test_gen получил: {result}")
    return "done"

# Проверяем тип
gen_obj = test_gen()
print(f"Тип test_gen(): {type(gen_obj)}")
print(f"Это генератор? {inspect.isgenerator(gen_obj)}")
print(f"Это корутина? {asyncio.iscoroutine(gen_obj)}")






























