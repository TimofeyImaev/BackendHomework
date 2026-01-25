import asyncio
import aiohttp
from aiostream import stream, pipe


async def main():
    users = [1, 2, 3, 4, 5]
    async with aiohttp.ClientSession() as session:
        async def fetch_posts(user_id):
            url = f'https://jsonplaceholder.typicode.com/posts/{user_id}'
            await asyncio.sleep(3)
            async with session.get(url) as response:
                await response.json()
                return "post " + str(user_id)
        
        async def fetch_photos(user_id):
            url = f'https://jsonplaceholder.typicode.com/photos/{user_id}'
            await asyncio.sleep(3)
            async with session.get(url) as response:
                await response.json()
                return "photo " + str(user_id)

        users_stream = stream.iterate(users)

        posts_stream = users_stream | pipe.map(fetch_posts)
        
        photos_stream = users_stream | pipe.map(fetch_photos)

        print("merge:")
        posts_and_photos = stream.chain(posts_stream, photos_stream)
        


        await stream.print(posts_and_photos)

        print("zip:")

        posts_and_photos = stream.zip(posts_stream, photos_stream)

        await stream.print(posts_and_photos)

if __name__ == "__main__":
    asyncio.run(main())

stream.merge()