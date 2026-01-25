import asyncio
from aiostream import stream, pipe
import aiohttp

requests_samples = [
    ('http://some-service/getItems/', {'user_id': 100}),  # вернет {'item_ids': [1, 2, 3]}
    ('http://some-service/getItems/', {'user_id': 101}),
]

service_1_url = 'http://service1/fillItems/'
service_2_url = 'http://service2/scoreItems/'
service_3_url = 'http://service3/logItems/'


def business_logic(service1_response, service2_response, service3_response) -> dict:
    # эта функция не делает сетевых вызовов, только обрабатывает ответы
    # считайте, что она уже написана
    return {}

async def getItems(url, params, session: aiohttp.ClientSession):
    async with session.get(url, params=params) as response:
        return await response.json()

async def postItems(url, data, session: aiohttp.ClientSession):
    async with session.post(url, json=data) as response:
        return await response.json()

async def main():
    connector = aiohttp.TCPConnector(
        limit=100,
        limit_per_host=30
    )
    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
        request_stream = stream.iterate(requests_samples)
        
        async def handleRequest(request) -> dict:
            try:
                item_ids = await getItems(request[0], request[1], session)

                responses = await asyncio.gather(
                     postItems(service_1_url, item_ids, session),
                     postItems(service_2_url, item_ids, session),
                     postItems(service_3_url, item_ids, session)
                )
                return business_logic(*responses)
            except Exception as e:
                print(f"Request failed: {e}")
                return None
        
        results_stream = request_stream \
            | pipe.map(handleRequest, task_limit=100) \
            | pipe.filter(lambda x: x is not None)
        
        results = await stream.list(results_stream)
        
        return results

asyncio.run(main())

def business_logic(service1_response, service2_response, service3_response) -> dict:
    # эта функция не делает сетевых вызовов, только обрабатывает ответы
    # считайте, что она уже написана
    return {}

async def getItems(url, params, session: aiohttp.ClientSession):
    async with session.get(url, params=params) as response:
        return await response.json()

async def postItems(url, data, session: aiohttp.ClientSession):
    async with session.post(url, data=data) as response:
        return await response



async def main():
    async with aiohttp.ClientSession() as session:
        results = []
        semaphore = asyncio.Semaphore(10)
        done = asyncio.Event()
        counter = 0

        async def handleRequest(request, session):
            nonlocal counter
            try:
                ...
            finally:
                counter += 1

                if counter == len(requests_samples):
                    done.set()
                semaphore.release()

        for request in requests_samples:
            await semaphore.acquire()
            asyncio.create_task(handleRequest(request, session))
        
        await done
        
        return results

asyncio.run(main())
asyncronous_iterable = [1, 2, 3, 4, 5]

a = stream.iterate(asyncronous_iterable)
a.map(lambda x: x * 2)
print(a.to_list())