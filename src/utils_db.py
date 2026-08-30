import json

import psycopg2
from src.views import AirplanesCords, CountryCords

from config import DB_CONFIG, COUNTRIES


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
                        "name varchar(100)"
                        ");")
        conn.close()

    def airplanes_table_creator(self):
        conn = psycopg2.connect(dbname=self.db_name, **DB_CONFIG)
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
        conn = psycopg2.connect(dbname=self.db_name, **DB_CONFIG)
        with conn:
            with conn.cursor() as cur:
                for country in COUNTRIES:
                    cur.execute("INSERT INTO country (name) VALUES (%s)"
                                "RETURNING id", (country, ))
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
                        print(airplane)



        conn.close()


if __name__ == '__main__':
    d = DBProector("aero")
    d.db_connection_test()
    d.db_creator()
    d.country_table_creator()
    d.insert_tables()
