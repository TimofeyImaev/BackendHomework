import asyncio
from aiostream import stream, pipe

async def streams():
    iterable = range(10)
    not_pipeline = stream.iterate(iterable)
    
    not_pipeline = stream.filter(not_pipeline, lambda x: x % 2 == 0)
    not_pipeline = stream.accumulate(not_pipeline, lambda x, y: x + y)
    
    print(await stream.list(not_pipeline))

async def pipelines():
    iterable = range(10)
    print(pipe.filter(lambda x: x % 2 == 0))

    pipeline = (
         pipe.filter(lambda x: x % 2 == 0)
        | pipe.accumulate(lambda x, y: x + y)
    )

    print(await stream.list(pipeline))
    
asyncio.run(pipelines())
asyncio.run(streams())
    