import websockets
import asyncio
import json

async def simple_client():
    uri = "wss://stream.binance.com/stream"
    async with websockets.connect(uri) as ws:
        subscribe = {"method": "SUBSCRIBE", "params": ["!miniTicker@arr@3000ms"], "id": 1}

        await ws.send(json.dumps(subscribe))

        while True:
            print(await ws.recv())

asyncio.run(simple_client())