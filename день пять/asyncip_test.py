import asyncio
from concurrent.futures import Future as ConcurrentFuture
from asyncio import Future as AsyncFuture

async def main1():
    print("main1_started")
    await asyncio.sleep(1)
    print("main1_started")
    
async def main2():
    print("main2_started")
    await asyncio.sleep(1)
    print("main2_ended")

async def run_all():
    t1 = asyncio.create_task(main1())
    t2 = asyncio.create_task(main2())

    await t1
    await t2

async def run_gather():
    await asyncio.gather(main1(), main2())

async def run_all_bad1():
    await main1()
    await main2()


async def run_all_bad2():
    t1 = main1()
    t2 = main2()
    await t1
    await t2

asyncio.run(run_all())

# Демонстрация Future классов
def show_futures():
    print("\n=== Сравнение Future классов ===\n")
    
    # concurrent.futures.Future - для синхронного кода с потоками/процессами
    print("1. concurrent.futures.Future:")
    print(f"   Тип: {ConcurrentFuture}")
    print(f"   Модуль: {ConcurrentFuture.__module__}")
    print("   Используется с: ThreadPoolExecutor, ProcessPoolExecutor")
    print("   Методы: .result(), .done(), .cancel(), .set_result()")
    
    # asyncio.Future - для асинхронного кода
    print("\n2. asyncio.Future:")
    print(f"   Тип: {AsyncFuture}")
    print(f"   Модуль: {AsyncFuture.__module__}")
    print("   Используется с: async/await, asyncio.create_task()")
    print("   Методы: .result(), .done(), .cancel(), .set_result(), await")
    
    print("\n=== Различия ===")
    print("- concurrent.futures.Future: блокирующий .result() (для потоков/процессов)")
    print("- asyncio.Future: неблокирующий, используется с await (для корутин)")
    print("- Они похожи по API, но работают в разных контекстах!")

if __name__ == "__main__":
    show_futures()