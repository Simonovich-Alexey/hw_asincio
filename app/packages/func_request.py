import requests


def get_person_count() -> int:
    http_response = requests.get(f'https://swapi.py4e.com/api/people/').json()
    person_count = http_response.get('count') + 20
    return person_count


async def get_items(client, request_key: str, name_key: str, json_result) -> str:
    if len(json_result.get(request_key)) != 0:
        if isinstance(json_result.get(request_key), str):
            http_response = await client.get(json_result.get(request_key))
            json_result = await http_response.json()
            return json_result.get(name_key)

        list_json = [await json_list.json() for json_list in
                     [await client.get(url_list) for url_list in json_result.get(request_key)]]
        list_result = [item.get(name_key) for item in list_json]
        return ', '.join(list_result)


async def get_person(client, person_id: int):
    http_response = await client.get(f'https://swapi.py4e.com/api/people/{person_id}/')
    json_result = await http_response.json()
    if not json_result.get('detail'):
        homeworld = await get_items(client, 'homeworld', 'name', json_result)
        films = await get_items(client, 'films', 'title', json_result)
        vehicles = await get_items(client, 'vehicles', 'name', json_result)
        starships = await get_items(client, 'starships', 'name', json_result)
        species = await get_items(client, 'species', 'name', json_result)
        json_result.update({'id': person_id,
                            'homeworld': homeworld,
                            'species': species,
                            'films': films,
                            'vehicles': vehicles,
                            'starships': starships})

        return json_result
    return {'status': 404}
