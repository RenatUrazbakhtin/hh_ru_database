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

def get_necessary_employers_data():
    list =[]
    for employer in get_employers_info():
        dict = {"title": employer["name"], "site_url": employer["site_url"]}
        list.append(dict)
    return list

def create_database(database_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"drop database if exists {database_name}")
    cur.execute(f"create database {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
	            employer_id SERIAL PRIMARY KEY,
	            title VARCHAR(255) NOT NULL,
                site_url VARCHAR(255)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            create table vacancies (
                    vacancy_id serial primary key,
                    vacancy_name varchar(255),
                    salary_from integer,
                    salary_to integer,
                    currency varchar(10),
                    employer varchar(255),
                    employer_id int,
                    vacancy_url varchar(255)
                    )
                    alter table vacancies
                    add constraint fk_vacancies_employers foreign_key(employer_id) references employers(employer_id)
                """)
    conn.commit()
    conn.close()

def save_data_employer_to_table(data, database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            cur.execute(
                """
                insert into employers (title, site_url)
                values (%s, %s)
                """,
                (employer['title'], employer['site_url'])
                )
    conn.commit()
    conn.close()

def save_data_vacancy_to_database(data, database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute(
                """
                insert into vacancies (vacancy_name, salary_from, salary_to, currency, employer, vacancy_url)
                values (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy['vacancy_name'], vacancy['salary_from'], vacancy['salary_to'], vacancy['currency'], vacancy['employer'], vacancy['vacancy_url'])
            )

    conn.commit()
    conn.close()
