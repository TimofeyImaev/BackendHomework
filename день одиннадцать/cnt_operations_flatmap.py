import asyncio
import aiohttp
from aiostream import stream, pipe

async def main():
    async with aiohttp.ClientSession() as session:
        counter_comments = 0
        counter_posts = 0
        max_concurrent_posts = 0
        max_concurrent_comments = 0
        async def fetch_post_comments(post):
            nonlocal counter_comments, max_concurrent_comments
            counter_comments += 1
            max_concurrent_comments = max(max_concurrent_comments, counter_comments)

            try:
                post_id = post["id"]
                url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}"
                async with session.get(url) as response:
                    comments = await response.json()
                    return comments
            finally:
                counter_comments -= 1
        
        async def fetch_user_posts(user_id):
            nonlocal counter_posts, max_concurrent_posts
            counter_posts += 1
            max_concurrent_posts = max(max_concurrent_posts, counter_posts)

            try:
                url = f"https://jsonplaceholder.typicode.com/posts?userId={user_id}"
                async with session.get(url) as response:
                    return await response.json()
            finally:
                counter_posts -= 1
        
        user_ids = range(1, 10)
        ids_stream = stream.iterate(user_ids)

        comments_stream = (ids_stream 
            | pipe.map(fetch_user_posts, task_limit=4)
             | pipe.flatmap(lambda x: stream.iterate(x))
             | pipe.map(fetch_post_comments, task_limit=4)
             | pipe.flatmap(lambda x: stream.iterate(x))
             | pipe.map(, ищем плохие слова)
        )
        await stream.print(comments_stream)

        print(f"Max concurrent requests: {max_concurrent_posts} {max_concurrent_comments}")

if __name__ == "__main__":
    asyncio.run(main())