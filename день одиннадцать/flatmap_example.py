import asyncio
import aiohttp
from aiostream import stream, pipe

async def main():
    async with aiohttp.ClientSession() as session:
        async def fetch_post_comments(post):
            post_id = post["id"]
            url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}"
            async with session.get(url) as response:
                comments = await response.json()
                return comments
        async def fetch_user_posts(user_id):
            url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
            async with session.get(url) as response:
                return await response.json()
        
        user_ids = range(1, 10)
        ids_stream = stream.iterate(user_ids)

        comments_stream = (ids_stream 
            | pipe.map(fetch_user_posts)
             | pipe.flatmap(lambda x: stream.iterate(x))
             | pipe.map(fetch_post_comments)
             | pipe.flatmap(lambda x: stream.iterate(x))
        )
        await stream.print(comments_stream)

if __name__ == "__main__":
    asyncio.run(main())