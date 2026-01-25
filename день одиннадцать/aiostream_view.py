import asyncio
import aiostream 
from aiostream import pipe

async def main():
    iterable = range(10)

    stream = aiostream.stream.iterate(iterable)

    await aiostream.stream.print(stream)

    stream = aiostream.stream.filter(stream, lambda x: x % 2 == 0)

    print(await aiostream.stream.list(stream))

    stream = aiostream.stream.accumulate(stream, lambda x, y: x + y)

    print(await aiostream.stream.take(stream, 5))
    print(await aiostream.stream.take(stream, 6))

    print(await aiostream.stream.list(stream))

asyncio.run(main())
