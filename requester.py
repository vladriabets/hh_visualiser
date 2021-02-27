import requests
import sys
from collections import Counter

def get_skills(text):
    '''Takes an input text and returns a list of all
    skills from hh.ru vacancies that contain this text'''

    base_path = 'https://api.hh.ru' + '/vacancies'

    specialization_path = base_path + '?area=2&specialization=1&text={}'.format(text)
    found = requests.get(specialization_path).json()['found']
    page = 0

    vacancies = []
    skills = []

    while (page - 1) * 100 < found:
        vacancies_pages_path = base_path +\
        '?area=2&specialization=1&per_page=100&page={}&text={}'.format(page, text)
        vacancies_pages_get = requests.get(vacancies_pages_path)
        for item in vacancies_pages_get.json()['items']:
            vacancies.append(item)
        page += 1

    for vacancy in vacancies:
        vacancy_id = vacancy['id']
        vacancies_path = base_path + '/' + vacancy_id
        response = requests.get(vacancies_path)
        skills.extend([skill['name'] for skill in response.json()['key_skills']])

    return skills


def get_most_demanded_items(number, items):
    '''Takes a list of items and returns a list with lenght = number,
    of the most common items from the list provided'''

    return Counter(items).most_common()[:number]

def main():
    main_text = sys.argv[1]
    try:
        main_number = int(sys.argv[2])
    except ValueError:
        print('Please enter number of skills after a secialization name')
        return 1

    main_skills = get_skills(main_text)
    return (get_most_demanded_items(main_number, main_skills))

if __name__ == "__main__":
    print(main())
