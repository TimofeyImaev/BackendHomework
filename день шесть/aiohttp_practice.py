import aiohttp
import asyncio

async def fetch_post(session, post_id, timeout):
    delay = 1
    while True:
        try:
            async with session.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}', timeout=timeout) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if 500 <= e.status < 600:
                await asyncio.sleep(delay)
                delay *= 2
                if delay > 16:
                    raise
            else:
                raise
        except (aiohttp.ClientConnectorError, aiohttp.ServerConnectionError, aiohttp.ClientOSError, asyncio.TimeoutError) as e:
            await asyncio.sleep(delay)
            delay *= 2
            if delay > 16:
                raise


async def main():
    async with aiohttp.ClientSession() as session:
        post = await fetch_post(session, 2, timeout=10)
        print(post)

asyncio.run(main())