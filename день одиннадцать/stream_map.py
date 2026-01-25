import asyncio
from aiostream import stream, pipe

async def streams():
    iterable = range(10)
    our_stream = stream.iterate(iterable)
    our_stream = stream.map(our_stream, lambda x: x * x)
    print(await stream.list(our_stream))

    
    our_stream = stream.iterate(iterable)
    our_stream = our_stream \
        | pipe.map(lambda x: x * x)
    print(await stream.list(our_stream))

asyncio.run(streams())