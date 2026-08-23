from src.views import CountyCords, AirplanesCords, AirplanesAnalyzer
from src.utils import JsonAirplaneStorage

def user_interaction():
    storage = JsonAirplaneStorage()

    while True:
        print("\n--- Система мониторинга самолетов ---")
        print("1. Запросить самолеты в стране (OpenSky)")
        print("2. Топ N самолетов по высоте из базы")
        print("3. Поиск самолетов по стране в базе")
        print("0. Выход")

        choice = input("Выбери действие: ")

        if choice == "1":
            country_name = input("Введите название страны на английском: ")

            geo = CountyCords("https://nominatim.openstreetmap.org/search", country_name)
            try:
                cords = geo.get_data()
                params = {
                "lamin": float(cords[0]), "lamax": float(cords[1]),
                "lomin": float(cords[2]), "lomax": float(cords[3]) }

                api = AirplanesCords('https://opensky-network.org/api/states/all', params)
                raw_data = api.get_data()

                if not raw_data.get('states'):
                    print("В этой зоне сейчас нет самолетов.")
                    continue

                for s in raw_data['states']:
                    plane_obj = AirplanesAnalyzer.from_opensky_vector(s)
                    plane_obj.validation()

                    plane_dict = plane_obj.__dict__
                    plane_dict['origin_country'] = country_name

                    storage.add_info(plane_dict)

                print(f"Успешно загружено {len(raw_data['states'])} самолетов.")

            except Exception as e:
                print(f"Ошибка при получении данных: {e}")

        elif choice == "2":
            try:
                n = int(input("Введите N для топа по высоте: "))
                data = storage.get_data()
                sorted_planes = sorted(data, key=lambda x: x.get('altitude') or 0, reverse=True)

                for p in sorted_planes[:n]:
                    print(f"ICAO: {p['icao']}, Позывной: {p['callsign']}, Высота: {p['altitude']} м")
            except ValueError:
                print("Введите корректное число.")

        elif choice == "3":
            country = input("Введите страну для поиска в базе: ")
            results = storage.get_data({"origin_country": country})
            for p in results:
                print(f"ICAO: {p['icao']}, Скорость: {p['velocity']}")

        elif choice == "0":
            break
