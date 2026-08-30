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
    #
    # def db_creator(self, db_name):
    #     conn = psycopg2.connect(dbname=db_name, **DB_CONFIG)
    #     conn.autocommit = True
    #     with conn.cursor() as cur:
    #         cur.execute(f"DROP DATABASE {db_name} IF EXISTS;")
    #         cur.execute(f"CREATE DATABASE {db_name};")
    #         db_version = cur.fetchone()
    #         print(f"БД {db_version} успешно создана!")
    #     conn.close()


if __name__ == '__main__':
    d = DBProector
    d.db_connection_test()
