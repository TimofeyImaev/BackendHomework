import asyncio
from types import coroutine
from asyncio.coroutines import iscoroutine
from types import coroutine

'''
# Старый стиль
@asyncio.coroutines
def old_style():
    yield from asyncio.sleep(1)
    return "done"

# Новый стиль
async def new_style():
    await asyncio.sleep(1)
    return "done"
'''

async def my_coroutine():
    return 42

@coroutine
def this_is_coroutine():
    return 52


# Вызываем корутинную функцию
coro = my_coroutine()
this_is_coro = my_coroutine()
print(type(coro))  # <class 'coroutine'>
print(iscoroutine(coro))  # 
print(iscoroutine(this_is_coro))