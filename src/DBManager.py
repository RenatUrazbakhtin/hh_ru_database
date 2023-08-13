import psycopg2
import config
class DBmanager():
    """
    Класс для работы с БД postgres
    """
    def __init__(self, database_name, params):
        """
        Инициялизатор класса
        :param database_name: Имя базы данных
        :param params: параметры подключения
        """
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        :return: список всех компаний и количество вакансий у каждой компании
        """
        with self.conn:
            list = []
            self.cur.execute("""select employer_id, title, count(vacancies.vacancy_id) as vacancies_number from employers join vacancies using(employer_id) group by employer_id""")
            data = self.cur.fetchall()
            for item in data:
                dict = {"employer_id": item[0], "title": item[1], "vacancies_number": item[2]}
                list.append(dict)
            return list

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        :return: список вакансий
        """
        with self.conn:
            list = []
            self.cur.execute(
                "select vacancy_id, employer, vacancy_name, salary_from, salary_to, vacancy_url from vacancies join employers using(employer_id)")
            data = self.cur.fetchall()
            for item in data:
                dict = {"vacancy_id": item[0], "employer": item[1], "vacancy_name": item[2], "salary_from": item[3],
                         "salary_to": item[4], "vacancy_url": item[5]}
                list.append(dict)
            return list

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        :return: средняя зарплата
        """
        with self.conn:
            self.cur.execute("select AVG((salary_from + salary_to)/2) as average_salary from vacancies")
            data = self.cur.fetchall()
        return int(data[0][0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: список вакансий
        """
        with self.conn:
            list = []
            self.cur.execute("select * from vacancies where (salary_from + salary_to)/2 > (select AVG((salary_from + salary_to)/2) from vacancies)")
            data = self.cur.fetchall()
            for item in data:
                dict = {"vacancy_id": item[0], "vacancy_name": item[1], "salary_from": item[2], "salary_to": item[3], "currency": item[4], "employer": item[5], "employer_id": item[6], "vacancy_url": item[7]}
                list.append(dict)
            return list

    def get_vacancies_with_keyword(self,search):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        :param search: поисковое слово
        :return: список вакансий
        """
        with self.conn:
            list = []
            self.cur.execute(f"select * from vacancies where vacancy_name like '%{search}%'")
            data = self.cur.fetchall()
            for item in data:
                dict = {"vacancy_id": item[0], "vacancy_name": item[1], "salary_from": item[2], "salary_to": item[3], "currency": item[4], "employer": item[5], "employer_id": item[6], "vacancy_url": item[7]}
                list.append(dict)
        return list