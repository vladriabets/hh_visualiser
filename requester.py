import requests


def get_vacancies(text):
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
    return vacancies


def count_key_skills(vacancies):
    key_skills_dict = dict()
    for vacancy in vacancies:
        vacancy_id = vacancy['id']
        path = 'https://api.hh.ru' + '/vacancies/' + vacancy_id
        response = requests.get(path)
        key_skills = [skill['name'] for skill in response.json()['key_skills']]
        for skill in key_skills:
            key_skills_dict.setdefault(skill, 0)
            key_skills_dict[skill] += 1
    return key_skills_dict


def get_most_demanded_skills(number, skills_dict):
    skills_list = []
    for key, value in skills_dict.items():
        if value > 1:
            skills_list.append((value, key))
    skills_list.sort(reverse=True)
    most_demanded = skills_list[:number]
    return most_demanded
