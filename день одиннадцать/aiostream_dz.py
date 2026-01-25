import asyncio
import aiohttp
from aiostream import stream, pipe

async def main():
    async with aiohttp.ClientSession() as session:
        async def get_posts(user_id):
            async with session.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}") as response:
                return await response.json()
        
        async def get_albums(user_id):
            async with session.get(f"https://jsonplaceholder.typicode.com/albums?userId={user_id}") as response:
                return await response.json()
        
        async def get_todos(user_id):
            async with session.get(f"https://jsonplaceholder.typicode.com/todos?userId={user_id}") as response:
                return await response.json()
        
        users = range(1, 10)
        users_stream = stream.iterate(users)

        async def post_type(post):
            post["type"] = "post"
            return post

        async def album_type(album):
            album["type"] = "album"
            return album

        async def todo_type(todo):
            todo["type"] = "todo"
            return todo
        
        posts_stream = users_stream | pipe.map(get_posts) \
            | pipe.flatmap(lambda x: stream.iterate(x)) \
                | pipe.map(post_type)
        albums_stream = users_stream | pipe.map(get_albums) \
            | pipe.flatmap(lambda x: stream.iterate(x)) \
                | pipe.map(album_type)
        todos_stream = users_stream | pipe.map(get_todos) \
            | pipe.flatmap(lambda x: stream.iterate(x)) \
                | pipe.map(todo_type)


        all_stream = stream.merge(posts_stream, albums_stream, todos_stream)

        posts = all_stream | pipe.filter(lambda x: x["type"] == "post")
        albums = all_stream | pipe.filter(lambda x: x["type"] == "album")
        todos = all_stream | pipe.filter(lambda x: x["type"] == "todo")

        await stream.print(posts)
        await stream.print(albums)
        await stream.print(todos)


if __name__ == "__main__":
    asyncio.run(main())