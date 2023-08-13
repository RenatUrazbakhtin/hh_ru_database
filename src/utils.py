###яндекс, ВК, деливери, Тинькоф, Сбер сервис, ВТБ, инфотекс, мтс, КРОК, АЙ-ТЕКО
import psycopg2
import requests, json
import config

# список id компаний
companies_id = [1740, 15478, 592442, 78638, 1473866, 4181, 3778, 3776, 2987, 115]
def get_hh_data_vacancy():
    """
    Получает данные о вакансиях через API
    :return: список данных
    """
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
    """
    Убирает лишнюю информацию о вакансиях
    :return: список вакансий
    """
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
    """
    Получает данные о работодателях через API
    :return: список работодателей
    """
    list = []
    for id in companies_id:
        request = requests.get(f"https://api.hh.ru/employers/{id}")
        data = request.json()
        list.append(data)
    return list

def get_necessary_employers_data():
    """
    Убирает лишнюю информацию о работодателях
    :return: список работодателей
    """
    list =[]
    for employer in get_employers_info():
        dict = {"title": employer["name"], "site_url": employer["site_url"]}
        list.append(dict)
    return list

def create_database(database_name, params):
    """
    Создает базу данных и создает таблицы employers, vacancies в postgresql
    :param database_name: имя базы данных
    :param params: параметры подключения
    """
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
                    employer_id int ,
                    vacancy_url varchar(255)
                    );
                    alter table vacancies
                    add constraint fk_vacancies_employers foreign key(employer_id) references employers(employer_id);
                """)
    conn.commit()
    conn.close()

def save_data_employer_to_database(data, database_name, params):
    """
    Заполняет таблицу employers полученными данными по API
    :param data: данные о работодателях
    :param database_name: имя базы данных
    :param params: параметры подключения
    """
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
    """
    Заполняет таблицу vacancies данных о вакансиях полученных по API
    :param data: данные о вакансиях
    :param database_name: имя базы данных
    :param params: параметры подключения
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute(
                """
                insert into vacancies (vacancy_name, salary_from, salary_to, currency, employer, vacancy_url)
                values (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy['vacancy_name'], vacancy['salary_from'], vacancy['salary_to'], vacancy['currency'], vacancy['employer'],  vacancy['vacancy_url'])
            )
            cur.execute("""
                update vacancies set employer_id = 1 where employer='Яндекс';
                update vacancies set employer_id = 2 where employer='VK';
                update vacancies set employer_id = 3 where employer='Маркет Деливери';
                update vacancies set employer_id = 4 where employer='Тинькофф';
                update vacancies set employer_id = 5 where employer='Сбербанк-Сервис';
                update vacancies set employer_id = 6 where employer='Банк ВТБ (ПАО)';
                update vacancies set employer_id = 7 where employer='ИнфоТеКС';
                update vacancies set employer_id = 8 where employer='МТС';
                update vacancies set employer_id = 9 where employer='КРОК';
                update vacancies set employer_id = 10 where employer='Ай-Теко (I-Teco)'; 
                """)

    conn.commit()
    conn.close()

