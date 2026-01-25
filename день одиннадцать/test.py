import asyncio
from aiostream import stream, pipe

async def test():
    counter = 0  # счетчик активных задач
    max_concurrent = 0  # максимум параллельных задач
    
    async def task(x):
        nonlocal counter, max_concurrent
        
        counter += 1
        current = counter
        max_concurrent = max(max_concurrent, current)

        if x % 4 == 0:
            await asyncio.sleep(10)
        await asyncio.sleep(0.5)
        print(f"Задача {x} начала работу. Одновременно работает: {current}")
        await asyncio.sleep(0.5)
        counter -= 1
        return x
    
    cur = stream.range(20)  # поток чисел от 0 до 9
    
    # task_limit=2 ограничивает параллелизм до 2 задач одновременно
    results = await stream.list(
        cur
        | pipe.map(task, task_limit=4, ordered=False)
    )

    # 0 1 2 3 4 5 6
    #  4 5 6 7
    # 
    # 
    # 

    print(f"Максимальное количество одновременно работающих задач: {max_concurrent}")
    print(f"Результаты: {results}")

asyncio.run(test())