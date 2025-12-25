import asyncio
import websockets

async def chat():
    async with websockets.connect("ws://localhost:8765") as ws:
        name = input("Name: ")
        await ws.send(name)
        
        asyncio.create_task(receive(ws))
        while True:
            message = await asyncio.get_event_loop().run_in_executor(None, input)
            await ws.send(message)

async def receive(ws):
    async for message in ws:
        print(message)

asyncio.run(chat())