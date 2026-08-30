import json

import psycopg2
from src.views import AirplanesCords, CountryCords

from config import DB_CONFIG, COUNTRIES


class DBProector:
    def __init__(self, db_name):
        self.__db_name = db_name

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
            cur.execute(f"DROP DATABASE IF EXISTS {self.__db_name};")
            cur.execute(f"CREATE DATABASE {self.__db_name};")
            # print(f"БД {self.db_name} успешно создана!")
        conn.close()

    def country_table_creator(self):
        conn = psycopg2.connect(dbname=self.__db_name, **DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE country"
                        "("
                        "id serial PRIMARY KEY,"
                        "name varchar(100)"
                        ");")
        conn.close()

    def airplanes_table_creator(self):
        conn = psycopg2.connect(dbname=self.__db_name, **DB_CONFIG)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE airplanes"
                        "("
                        "icao varchar(10) PRIMARY KEY,"
                        "callsign varchar(50),"
                        "registration varchar(100),"
                        "velocity float,"
                        "altitude float,"
                        "dislocation int REFERENCES country(id)"
                        ");")
        conn.close()

    def insert_tables(self):
        conn = psycopg2.connect(dbname=self.__db_name, **DB_CONFIG)
        with conn:
            with conn.cursor() as cur:
                for country in COUNTRIES:
                    cur.execute("INSERT INTO country (name) VALUES (%s)"
                                "RETURNING id", (country,))
                    country_id = cur.fetchone()[0]
                    # print(country_id)
                    sqrt = CountryCords("https://nominatim.openstreetmap.org/search", country)
                    country_cords = sqrt.get_data()
                    # countries_data = json.dumps(countries_a, indent=4, ensure_ascii=False)

                    params = {
                        "lamin": float(country_cords[0]),
                        "lamax": float(country_cords[1]),
                        "lomin": float(country_cords[2]),
                        "lomax": float(country_cords[3])
                    }

                    airplanes = AirplanesCords('https://opensky-network.org/api/states/all', params)
                    airplanes_data = airplanes.get_data()
                    for airplane in airplanes_data.get("states"):
                        cur.execute(
                            "INSERT INTO airplanes (icao, callsign, registration, velocity, altitude, dislocation) VALUES (%s, %s, %s, %s, %s, %s)"
                            , (airplane[0], airplane[1].strip(), airplane[2], airplane[9], airplane[7], country_id))

        conn.close()


class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def execute_query(self, query):
        conn = psycopg2.connect(dbname=self.__db_name, **DB_CONFIG)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_countries_and_aeroplanes_count(self):
        """получает список всех стран и количество самолетов в их воздушных пространствах"""
        return self.execute_query("""SELECT COUNT(*), country.name FROM airplanes 
                                     JOIN country ON airplanes.dislocation=country.id
                                     GROUP BY country.id, country.name""")

    def get_all_aeroplanes(self):
        """получает список всех воздушных судов."""
        return self.execute_query("SELECT * FROM airplanes")

    def get_avg_speed(self):
        """получает среднюю скорость по самолетам"""
        return self.execute_query("SELECT AVG(velocity) FROM airplanes")

    def get_aeroplanes_with_higher_speed(self):
        """получает список всех самолетов, у которых скорость выше средней"""
        return self.execute_query("""SELECT * FROM airplanes
                                     WHERE velocity > (SELECT AVG(velocity) FROM airplanes)""")

    def get_aeroplanes_with_keyword(self, finder_str):
        """получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        return self.execute_query(f"SELECT * FROM airplanes WHERE callsign LIKE '{finder_str}%'")


if __name__ == '__main__':
    d = DBProector("aero")
    d.db_connection_test()
    d.db_creator()
    d.country_table_creator()
    d.airplanes_table_creator()
    d.insert_tables()

    manager = DBManager("aero")
    print(manager.get_aeroplanes_with_keyword("ACA"))
