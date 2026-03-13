import requests
import asyncio, aiohttp
from itertools import batched
from db import Base, SwapiPerson, engine, Session, init_orm, close_orm
import pprint

MAX_REQUESTS = 5

def get_info(url_list):
    final_list = []
    for url in url_list:
        info_json = requests.get(url).json()
        first_key = list(info_json.keys())[0]
        final_list.append(info_json[first_key])
    return final_list


async def insert_in_db(person_list_json):
    person_list = [SwapiPerson(
        birth_year=person["birth_year"],
        eye_color=person["eye_color"],
        gender=person["gender"],
        hair_color=person["hair_color"],
        homeworld=person["homeworld"],
        mass=person["mass"],
        name=person["name"],
        skin_color=person["skin_color"],
        ) for person in person_list_json]
    pprint.pprint(person_list)

    async with Session() as db_session:
        db_session.add_all(person_list)
        await db_session.commit()



async def get_person(person_id: int, session: aiohttp.ClientSession):
    http_response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    # http_response = await session.get(f"https://www.swapi.tech/api/people/{person_id}/")
    json_data = await http_response.json()
    # print(json_data)
    return json_data


async def main():
    await init_orm()

    async with aiohttp.ClientSession() as session:
        for person_id_batched in batched(range(1, 101), MAX_REQUESTS):
            coros = []
            for person_id in person_id_batched:
                person_coro = get_person(person_id, session)
                if person_coro is not None:
                    coros.append(person_coro)
            response = await asyncio.gather(*coros)
            insert_in_db_coro = insert_in_db(response)
            asyncio.create_task(insert_in_db_coro)

    all_tasks = asyncio.all_tasks()
    main_task = asyncio.current_task()
    all_tasks.remove(main_task)
    for task in all_tasks:
        await task
    await close_orm()


if __name__ == '__main__':
    asyncio.run(main())
    print('Everything is ok')