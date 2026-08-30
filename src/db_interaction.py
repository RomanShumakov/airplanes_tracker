from src.utils_db import DBProector, DBManager
import io
from contextlib import redirect_stdout
import os
os.environ['LC_MESSAGES'] = 'C'

import psycopg2
from src.views import AirplanesCords, CountryCords

from config import DB_CONFIG, COUNTRIES

def database_interaction():
    while True:
        db_name = input("Введите желаемое имя базы данных: ").strip()
        db_obj = DBProector(db_name)

        f = io.StringIO()
        try:
            with redirect_stdout(f):
                db_obj.db_connection_test()
            output = f.getvalue()
            print(output.strip())
        except Exception:
            raise ConnectionError("Введены неверные учетные данные. Доступ заблокирован.") from None


        db_obj.db_creator()
        db_obj.country_table_creator()
        db_obj.airplanes_table_creator()
        print(f"БД {db_name} успешно создана!")
        print(f"Начинаю заполнение данными самолетов...")
        db_obj.insert_tables()
        print(f"Самолеты добавлены!")
        # print("\n--- Система работы с БД ---")
        # print("1. Получить список всех стран и количество самолетов в их воздушных пространствах")
        # print("2. Получить список всех воздушных судов")
        # print("3. Топ N самолетов по высоте из базы")
        # print("4. Поиск самолетов по стране в базе")
        # print("0. Выход")
#
# manager = DBManager("aero")
# print(manager.get_aeroplanes_with_keyword("ACA"))

if __name__ == '__main__':
    database_interaction()