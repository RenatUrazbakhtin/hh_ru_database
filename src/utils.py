###яндекс, ВК, деливери, Тинькоф, Сбер сервис, ВТБ, инфотекс, мтс, КРОК, АЙ-ТЕКО
import psycopg2
import requests, json
def get_hh_data_vacancy():
    companies_id = [1740, 15478, 592442, 78638, 1473866, 4181, 3778, 3776, 2987, 115]
    list = []
    for id in companies_id:
        params = {
            'employer_id': id,
            'per_page': 30
        }
        request = requests.get("https://api.hh.ru/vacancies", params=params)
        data = request.json()['items']
        list.append(data)
    return list


def get_necessary_vacancy_info():
    list = []
    for item in get_hh_data_vacancy():
        for vacancy in item:
            dict = {"vacancy_name": vacancy['name'], "salary": vacancy['salary'],
                    "employee": vacancy['employer']['name'], "vacancy_url": vacancy['alternate_url'],
                    "employment": vacancy['employment']['name'], "experience": vacancy['experience']['name'],
                    "requirements": vacancy['snippet']['requirement']}
            list.append(dict)
    return list


