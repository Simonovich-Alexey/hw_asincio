import requests


def get_person_count():
    http_response = requests.get(f'https://swapi.py4e.com/api/people/').json()
    person_count = http_response.get('count') + 20
    return person_count


async def get_person(client, person_id):
    http_response = await client.get(f'https://swapi.py4e.com/api/people/{person_id}/')
    json_result = await http_response.json()
    if not json_result.get('detail'):
        json_result.update({'id': person_id})
        return json_result
    return {'status': 404}
