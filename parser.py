import requests
from pprint import pprint
import json

dictionaries = requests.get('https://api.hh.ru/dictionaries')
pprint(json.loads(dictionaries.text))

#response = requests.get('https://api.hh.ru' + '/vacancies')
#pprint(response.text)