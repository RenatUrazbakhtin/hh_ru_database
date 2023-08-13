from src.DBManager import DBmanager
import src.utils
from config import config

if __name__ == "__main__":
    param = config()
    database_name = "NEW_DATABASE"


    employers_data = src.utils.get_necessary_employers_data()
    vacancy_data = src.utils.get_necessary_vacancy_info()

    src.utils.create_database(database_name, param)

    src.utils.save_data_employer_to_database(employers_data, database_name, param)
    src.utils.save_data_vacancy_to_database(vacancy_data, database_name, param)

    dbmanager = DBmanager(database_name, param)
    # Ввести желаемые методы класса DBmanager(get_companies_and_vacancies_count, get_all_vacancies, get_avg_salary, get_vacancies_with_higher_salary, get_vacancies_with_keyword)

