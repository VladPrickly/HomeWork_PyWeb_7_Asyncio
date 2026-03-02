import requests
import asyncio, aiohttp

async def get_info(person_id: int):
    session = aiohttp.ClientSession()
    http_response = await session.get(f"https://www.swapi.tech/api/people/{person_id}/")
    json_data = await http_response.json()
    await session.close()
    return json_data


async def main():
    coro_1 = get_info(1)
    coro_2 = get_info(2)

    response = await asyncio.gather(coro_1, coro_2)

    print(response)

asyncio.run(main())