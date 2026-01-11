import aiohttp
import asyncio
import datetime

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            async def random_query():
                try:
                    async with session.get("http://peaceful_robinson:8000/random") as response:
                        return await response.text()
                except Exception as e:
                    print(e)
                    return []
            tasks = [asyncio.create_task(random_query()) for _ in range(50)]

            str_now_time = datetime.datetime.now().__str__()
            
            responses = await asyncio.gather(*tasks)
            str_responses = ' '.join(responses)

            with open('data/responses', 'a', encoding='utf-8') as f:
                f.write(f"\n{str_now_time}:{str_responses}")

            print("INFO: Done one iteration")
            await asyncio.sleep(1)


asyncio.run(main())