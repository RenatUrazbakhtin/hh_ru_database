###яндекс, ВК, деливери, Тинькоф, Сбер сервис, ВТБ, инфотекс, мтс, КРОК, АЙ-ТЕКО
import psycopg2
import requests, json
import config

companies_id = [1740, 15478, 592442, 78638, 1473866, 4181, 3778, 3776, 2987, 115]
def get_hh_data_vacancy():
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
            dict = {"vacancy_name": vacancy['name'],
                    "employer": vacancy['employer']['name'], "vacancy_url": vacancy['alternate_url'],
                    }
            list.append(dict)

            if vacancy['salary'] is None:
                dict['salary_from'] = 0
                dict['salary_to'] = 0
                dict['currency'] = 'Нет валюты'
            else:
                if vacancy['salary']['from'] is None:
                    dict['salary_from'] = 0
                else:
                    dict['salary_from'] = vacancy['salary']['from']

                if vacancy['salary']['to'] is None:
                    dict['salary_to'] = 0
                else:
                    dict['salary_to'] = vacancy['salary']['to']
                if vacancy['salary']['currency'] == 'RUR':
                    dict['currency'] = 'RUB'
                else:
                    dict['currency'] = vacancy['salary']['currency']
    return list


def get_employers_info():
    list = []
    for id in companies_id:
        request = requests.get(f"https://api.hh.ru/employers/{id}")
        data = request.json()
        list.append(data)
    return list


