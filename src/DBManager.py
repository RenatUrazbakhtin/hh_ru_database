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




