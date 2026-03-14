import requests
import asyncio, aiohttp
from itertools import batched
from db import SwapiPerson, Session, init_orm, close_orm, drop_orm
import pprint
import datetime

MAX_REQUESTS = 25


def get_info(url_list):
    final_list = []
    for url in url_list:
        info_json = requests.get(url).json()
        first_key = list(info_json.keys())[0]
        final_list.append(info_json[first_key])
    return final_list


async def insert_in_db(person_list_json):
    person_list = [SwapiPerson(
        birth_year=person.get("birth_year"),
        eye_color=person.get("eye_color"),
        gender=person.get("gender"),
        hair_color=person.get("hair_color"),
        homeworld=person.get("homeworld"),
        mass=person.get("mass"),
        name=person.get("name"),
        skin_color=person.get("skin_color"),
    ) for person in person_list_json]
    # Вывод информации на экран для осуществления текущего контроля
    print("-" * 50)
    print("Next list of Start Wars person to add Database")
    print("-" * 50)
    pprint.pprint(person_list)

    async with Session() as db_session:
        db_session.add_all(person_list)
        await db_session.commit()


async def get_person(person_id: int, session: aiohttp.ClientSession):
    http_response = await session.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    # http_response = await session.get(f"https://www.swapi.tech/api/people/{person_id}/")
    json_data = await http_response.json()
    # pprint.pprint((json_data))
    return json_data


async def main():
    await drop_orm()
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
    print('Process successfully started')
    start = datetime.datetime.now()
    asyncio.run(main())
    print('Process successfully finished')
    print(f'Total time: {(datetime.datetime.now() - start)}')
