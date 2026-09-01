from src.utils_db import DBProector, DBManager
import io
from contextlib import redirect_stdout


def database_interaction():
    """Функция для работы c БД через пользовательский интерфейс"""
    db_name = input("Введите желаемое имя базы данных: ").strip()
    db_obj = DBProector(db_name)

    # Проверка правильности ввода учетных данных (опционально)
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            db_obj.db_connection_test()
        output = f.getvalue()
        print(output.strip())
    except Exception:
        raise ConnectionError("Введены неверные учетные данные. Доступ заблокирован. Проверьте файл '.env'.") from None

    db_obj.db_creator()
    db_obj.country_table_creator()
    db_obj.airplanes_table_creator()
    print(f"БД {db_name} успешно создана!")
    print(f"Начинаю заполнение данными самолетов...")
    db_obj.insert_tables()
    print(f"Самолеты добавлены!")
    while True:
        print("\n--- Система работы с БД ---")
        print("1. Получить список всех стран и количество самолетов в их воздушных пространствах")
        print("2. Получить список всех воздушных судов")
        print("3. Получить среднюю скорость по самолетам")
        print("4. Получить список всех самолетов, у которых скорость выше средней")
        print("5. Получает список всех самолетов, в позывном которых содержатся переданные символы")
        print("0. Выход")

        user_input = input()
        db_manager = DBManager(db_name)
        if user_input == "1":
            print(db_manager.get_countries_and_aeroplanes_count())
        elif user_input == "2":
            print(db_manager.get_all_aeroplanes())
        elif user_input == "3":
            print(db_manager.get_avg_speed()[0][0])
        elif user_input == "4":
            print(db_manager.get_aeroplanes_with_higher_speed())
        elif user_input == "5":
            user_input = input("Введите символы для поиска: ")
            print(db_manager.get_aeroplanes_with_keyword(user_input))
        elif user_input == "0":
            break
        else:
            print("Неопознанная команда. Повторите ввод.")


if __name__ == '__main__':
    database_interaction()
