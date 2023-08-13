import psycopg2
import config
class DBmanager():
    def __init__(self, database_name, params):
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        with self.conn:
            self.cur.execute("""select employer_id, title, count(vacancies.vacancy_id) as vacancies_number from employers join vacancies using(employer_id) group by employer_id""")
            data = self.cur.fetchall()
            for item in data:
                dict = [{"employer_id": item[0], "title": item[1], "vacancies_number": item[2]}]
        return dict

    def get_all_vacancies(self):
        with self.conn:
            self.cur.execute(
                "select vacancy_id, employer, vacancy_name, salary_from, salary_to, vacancy_url from vacancies join employers using(employer_id)")
            data = self.cur.fetchall()
            for item in data:
                dict = [{"vacancy_id": item[0], "employer": item[1], "vacancy_name": item[2], "salary_from": item[3],
                         "salary_to": item[4], "vacancy_url": item[5]}]
        return dict


