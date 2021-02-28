import requests
import sys
import asyncio
import aiohttp
from collections import Counter

async def get_skills(text):
    '''Takes an input text and returns a list of all
    skills from hh.ru vacancies that contain this text'''

    base_path = 'https://api.hh.ru' + '/vacancies'

    specialization_path = base_path + '?area=2&specialization=1&text={}'.format(text)

    page = 0
    vacancies = []
    skills = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(specialization_path) as response:
            found = await response.json()
            found = found['found']

        while (page - 1) * 100 < found:
            vacancies_pages_path = base_path +\
            '?area=2&specialization=1&per_page=100&page={}&text={}'.format(page, text)
            async with session.get(vacancies_pages_path) as vacancies_pages_get:
                vacancies_pages_get = await vacancies_pages_get.json()
            for item in vacancies_pages_get['items']:
                vacancies.append(item)
            page += 1

        for vacancy in vacancies:
            vacancy_id = vacancy['id']
            vacancies_path = base_path + '/' + vacancy_id
            async with session.get(vacancies_path) as response:
                response_json = await response.json()
            skills.extend([skill['name'] for skill in response_json['key_skills']])

    return skills


async def get_most_demanded_items(number, items):
    '''Takes a list of items and returns a list with lenght = number,
    of the most common items from the list provided'''

    return Counter(items).most_common()[:number]

async def main():
    main_text = sys.argv[1]
    try:
        main_number = int(sys.argv[2])
    except ValueError:
        print('Please enter number of skills after a secialization name')
        return 1

    main_skills = await get_skills(main_text)
    result = await get_most_demanded_items(main_number, main_skills)
    print(result)
    return result

if __name__ == "__main__":
    asyncio.run(main())
