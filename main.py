import requests
import asyncio, aiohttp
from itertools import batched

MAX_REQUESTS = 5

async def get_info(person_id: int, session: aiohttp.ClientSession):
    http_response = await session.get(f"https://www.swapi.tech/api/people/{person_id}/")
    json_data = await http_response.json()
    return json_data


async def main():
    async with aiohttp.ClientSession() as session:
        for id_b in batched(range(1, 101), MAX_REQUESTS):
            coros = []
            for i in id_b:
                coro = get_info(i, session)
                coros.append(coro)
            response = await asyncio.gather(*coros)

            print(response)

asyncio.run(main())