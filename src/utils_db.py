import psycopg2

from config import DB_CONFIG

class DBProector:
    def __init__(self, db_name):
        self.db_name = db_name

    @staticmethod
    def db_connection_test():
        conn = psycopg2.connect(dbname="postgres", **DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            print(f"Успешное подключение! Версия БД: {db_version}")
        conn.close()

    def db_creator(self):
        conn = psycopg2.connect(dbname="postgres", **DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {self.db_name};")
            cur.execute(f"CREATE DATABASE {self.db_name};")
            # print(f"БД {self.db_name} успешно создана!")
        conn.close()

    def country_table_creator(self):
        conn = psycopg2.connect(dbname=self.db_name, **DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE country"
                        "("
                        "id serial PRIMARY KEY,"
                        "country varchar(100)"
                        ");")
        conn.close()


if __name__ == '__main__':
    d = DBProector("aero")
    # d.db_connection_test()
    # d.db_creator()
    d.country_table_creator()
