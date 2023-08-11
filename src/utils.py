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
            dict = {"vacancy_name": vacancy['name'],
                    "employee": vacancy['employer']['name'], "vacancy_url": vacancy['alternate_url'],
                    "employment": vacancy['employment']['name'], "experience": vacancy['experience']['name'],
                    "requirements": vacancy['snippet']['requirement']}
            list.append(dict)

            if vacancy['salary'] is None:
                dict['salary_from'] = 0
                dict['salary_to'] = 0
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


def get_emploee_info():
    list = []
    companies_id = [1740, 15478, 592442, 78638, 1473866, 4181, 3778, 3776, 2987, 115]
    for id in companies_id:
        request = requests.get(f"https://api.hh.ru/employers/{id}")
        data = request.json()
        list.append(data)
    return list

# def create_database(database_name, params):
#     conn = psycopg2.connect(dbname='postgres', **params)
#     conn.autocommit = True
#     cur = conn.cursor()
#
#     cur.execute(f"DROP DATABASE {database_name}")
#     cur.execute(f"CREATE DATABASE {database_name}")
#
#     conn.close()
#
#     conn = psycopg2.connect(dbname=database_name, **params)
#
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE employee (
#                     employee_id serial primary key,
#                     title VARCHAR(255) not null,
#                     description text
#                     site_url varchar(255),
#                     open_vacancies integer
#                     )
#         """)
#
#     with conn.cursor() as cur:
#         cur.execute("""
#             create table vacancy (
#                     vacancy_id serial primary_key,
#                     vacancy_name varchar(255),
#                     salary integer
#                     employee varchar(255) references title
#                     vacancy_url varchar(255)
#                     employment varchar(255)
#                     experience varchar(255)
#                     requirements text
# )