import requests
from pprint import pprint
import json

text = 'python'
base_path = 'https://api.hh.ru' + '/vacancies' + \
        '?area=2&specialization=1&text={}'.format(text)
base = requests.get(base_path)
found = base.json()['found']
page = 0
vacancies = []
while (page - 1) * 100 < found:
    path = 'https://api.hh.ru' + '/vacancies' + \
            '?area=2&specialization=1&per_page=100&page={}&text={}'.format(page, text)
    response = requests.get(path)
    for i in response.json()['items']:
        vacancies.append(i)
    page += 1

pprint(vacancies[1])

#dictionaries = requests.get('https://api.hh.ru/dictionaries')
#pprint(json.loads(dictionaries.text))