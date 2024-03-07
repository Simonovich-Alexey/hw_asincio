import asyncio
import datetime

import aiohttp
from more_itertools import chunked
from packages.models import init_db, Person, Session, engine
from packages.func_request import get_person_count, get_person

MAX_CHUNK = 10


async def insert_to_db(item_json):
    models = [Person(id=item.get('id'),
                     birth_year=item.get('birth_year'),
                     eye_color=item.get('eye_color'),
                     films=item.get('films'),
                     gender=item.get('gender'),
                     hair_color=item.get('hair_color'),
                     height=item.get('height'),
                     homeworld=item.get('homeworld'),
                     mass=item.get('mass'),
                     name=item.get('name'),
                     skin_color=item.get('skin_color'),
                     species=item.get('species'),
                     starships=item.get('starships'),
                     vehicles=item.get('vehicles')
                     ) for item in item_json if not item.get('status')]
    async with Session() as session:
        session.add_all(models)
        await session.commit()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, get_person_count()), MAX_CHUNK):
        coro = [get_person(client, person_id) for person_id in chunk]
        result = await asyncio.gather(*coro)
        asyncio.create_task(insert_to_db(result))

    tasks_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_set)

    await client.close()
    await engine.dispose()


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)
