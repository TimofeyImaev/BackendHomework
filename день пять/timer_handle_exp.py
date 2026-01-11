import asyncio
import time

def callback(name):
    print(f"{name} called at {time.time()}")

async def main():
    loop = asyncio.get_event_loop()
    
    # Создаем таймеры
    loop.call_later(1.0, callback, "Timer1")  # через 1 сек
    loop.call_at(loop.time() + 2.0, callback, "Timer2")  # через 2 сек
    
    # Можем отменить
    # timer1.cancel()
    
    # Ждем выполнения
    await asyncio.sleep(3)

asyncio.run(main())