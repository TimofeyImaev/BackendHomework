import asyncio
from types import coroutine

async def test_await():
    """Тестируем await"""
    future = asyncio.Future()
    future.set_result(42)
    
    # await вызывает __await__()
    result = await future
    print(f"await результат: {result}")  # 42

@coroutine
def test_yield_from():
    """Тестируем yield from (старый стиль)"""
    future = asyncio.Future()
    future.set_result(42)
    
    # yield from вызывает __iter__(), который равен __await__()
    result = yield from future
    print(f"yield from результат: {result}")  # 42

# Запускаем оба
loop = asyncio.get_event_loop()
loop.run_until_complete(test_await())
loop.run_until_complete(test_yield_from())