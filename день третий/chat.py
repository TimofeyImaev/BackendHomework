import asyncio
import websockets

clients = {}

async def chat(websocket):
    name = await websocket.recv()
    clients[websocket] = name
    
    try:
        async for message in websocket:
            await asyncio.gather(*[client.send(f"{name}: {message}") for client in clients])
    finally:
        del clients[websocket]

async def main():
    async with websockets.serve(chat, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())