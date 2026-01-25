import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        token = ""
        async with session.post("http://localhost:8000/task", json={"payload":{}, "priority": 2}) as resp:
            token = await resp.json()
            print(token["task_id"])
            token = token["task_id"]
        async with session.get(f'http://localhost:8000/task/{token}') as resp:
            print(await resp.text())
        await asyncio.sleep(3)
        async with session.get(f'http://localhost:8000/task/{token}') as resp:
            print(await resp.text())
        await asyncio.sleep(3)
        async with session.get(f'http://localhost:8000/task/{token}') as resp:
            print(await resp.text())
        await asyncio.sleep(3)
        async with session.get(f'http://localhost:8000/task/{token}') as resp:
            print(await resp.text())

asyncio.run(main())