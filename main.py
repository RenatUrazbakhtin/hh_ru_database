from src.DBManager import DBmanager
from src.utils import save_data_employer_to_database, save_data_vacancy_to_database, get_necessary_employers_data, get_necessary_vacancy_info, create_database
from config import config
def main():
    """
    собирает в единую программу все функции и файлы
    """
    # данные для создания БД
    param = config()
    database_name = "itsworking"

    # создание БД и таблиц
    create_database(database_name, param)

    # Получение данных по API
    employers_data = get_necessary_employers_data()
    vacancy_data = get_necessary_vacancy_info()

    # Запись данных в таблицы
    save_data_employer_to_database(employers_data, database_name, param)
    save_data_vacancy_to_database(vacancy_data, database_name, param)

    # Создание экземпляра класса DMmanager для работы с БД
    dbmanager = DBmanager(database_name, param)

    # Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    for item in dbmanager.get_companies_and_vacancies_count():
        print(item)
    print("\n\n\n")

    # Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
    for item in dbmanager.get_all_vacancies():
        print(item)
    print("\n\n\n")

    # Получает среднюю зарплату по вакансиям.
    print(dbmanager.get_avg_salary())
    print("\n\n\n")

    # Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
    for item in dbmanager.get_vacancies_with_higher_salary():
        print(item)
    print("\n\n\n")

    # Получает список всех вакансий, в названии которых содержатся переданные в метод слова
    search = input("Введите слово для поиска ")
    for item in dbmanager.get_vacancies_with_keyword(search):
        print(item)
    print("\n\n\n")

if __name__ == '__main__':
    main()

