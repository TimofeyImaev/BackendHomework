import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from typing import Iterable, Coroutine, Tuple, List, Any
from asyncio import Semaphore
import aiohttp
import aiofiles

async def run_with_timeout(coros: Iterable[Coroutine], timeout: float) -> Tuple[List[Any], int]:
    """
    Запускает корутины параллельно как задачи, ждёт либо завершения всех, либо наступления timeout.
    Возвращает список результатов успешно завершённых задач (порядок не обязателен) и количество отменённых задач.
    При отмене гарантирует, что внутри корутин выполнится их cleanup (если есть).
    """
    tasks = [asyncio.create_task(coro) for coro in coros]
    done, pending = await asyncio.wait(tasks, timeout=timeout)

    cancelled_count = 0
    for task in pending:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            cancelled_count += 1

    results = []
    for task in done:
        if task.exception() is None:
            results.append(task.result())
        else:
            raise task.exception()

    return results, cancelled_count


import aiohttp
import aiofiles

async def fetch_url(url, session):
    async with session.get(url) as response:
        return await response.text()

async def save_response(response, index):
    async with aiofiles.open(f'responses{index}.txt', "a") as f:
        await f.write(response)

async def scrapper(urls, max_concurrency):
    async with aiohttp.ClientSession() as session:
        semaphore = Semaphore(max_concurrency)
        cnt_tasks = 0
        event = asyncio.Event()
        
        async def fetch_and_save(url, index):
            nonlocal cnt_tasks
            try:
                response = await fetch_url(url, session)
                await save_response(response, index)
            finally:
                semaphore.release()
                cnt_tasks += 1
                if cnt_tasks == len(urls):
                    event.set()

        for i in range(len(urls)):
            
            await semaphore.acquire()
            asyncio.create_task(fetch_and_save(urls[i], i))
        
        await event.wait()

import threading


async def file_writer_async(filename, data):
    done = asyncio.Future()
    loop = asyncio.get_event_loop()

    def file_writer(filename, data):
        with open(filename, "a") as f:
            f.write(data)
            loop.call_soon_threadsafe(done.set_result, None)

    thread = threading.Thread(target=file_writer, args=(filename, data))
    thread.start()

    await done


async def main():
    cnt = 1000
    st = time.time()

    for _ in range(cnt):
        await file_writer_async("rand1.txt", "1")

    print(time.time() - st)

    st = time.time()
    for _ in range(cnt):
        async with aiofiles.open("rand2.txt", "a") as f:
            await f.write("2")

    print(time.time() - st)

asyncio.run(main())