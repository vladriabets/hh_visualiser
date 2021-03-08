import sys
import asyncio
import aiohttp
from time import time
from collections import Counter


# async functions

async def request_json(url, session):
    async with session.get(url) as response:
        json_result = await response.json()
        return json_result


async def get_vacancies(base_path, text, session):
    specialization_path = base_path + '?area=2&specialization=1&text={}'.format(text)
    response_specs = await request_json(specialization_path, session)
    found = response_specs['found']
    pages = [i for i in range(int((found / 100) + 1))]

    vacancies = []
    tasks = []

    for page in pages:
        vacancies_pages_path = base_path + \
                               '?area=2&specialization=1&per_page=100&page={}&text={}'.format(page, text)
        task = asyncio.create_task(request_json(vacancies_pages_path, session))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    for vacancies_pages in results:
        vacancies.extend([item for item in vacancies_pages['items']])

    return vacancies


async def get_skills(base_path, vacancies, session):
    skills = []
    tasks = []

    for vacancy in vacancies:
        vacancy_path = base_path + '/' + vacancy['id']
        task = asyncio.create_task(request_json(vacancy_path, session))
        tasks.append(task)

    results = await asyncio.gather(*tasks)

    for vacancies_json in results:
        try:
            skills.extend([skill['name'] for skill in vacancies_json['key_skills']])
        except KeyError:
            continue

    return skills


# sync functions

def get_most_demanded_items(number, items):
    return Counter(items).most_common()[:number]


def get_args():
    try:
        text = sys.argv[1]
        number = int(sys.argv[2])

    except IndexError:
        print('Please enter a specialization and number of skills')
        raise SystemExit(1)

    except ValueError:
        print('Please enter number of skills after a specialization')
        raise SystemExit(1)

    return text, number


# entry point

async def main():
    t0 = time()

    main_text_and_num = get_args()
    main_text = main_text_and_num[0]
    main_number = main_text_and_num[1]

    base_path = 'https://api.hh.ru' + '/vacancies'
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    vacancies = await get_vacancies(base_path, main_text, session)
    skills = await get_skills(base_path, vacancies, session)
    items = get_most_demanded_items(main_number, skills)

    await session.close()

    end_time = time()

    print(end_time - t0)
    print(items)
    return items


if __name__ == "__main__":
    asyncio.run(main())
