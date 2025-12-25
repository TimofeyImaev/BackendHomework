import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f'Sever received: {name}')

    greetings = f'Hello {name}'

    await websocket.send(greetings)
    print(f'Server sent: {greetings}')

async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main());