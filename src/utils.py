import json
import os
from abc import ABC, abstractmethod


class AirplanesStorage(ABC):

    @abstractmethod
    def add_info(self, airplane):
        pass

    @abstractmethod
    def get_data(self, criteria=None):
        pass

    @abstractmethod
    def delete_info(self, icao):
        pass

    @abstractmethod
    def clear_all(self):
        pass


class JsonAirplaneStorage(AirplanesStorage):
    """Класс для операций с самолетами в json-файле"""

    def __init__(self, filename="airplanes.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as new_file:
                json.dump([], new_file)

    def add_info(self, airplane):
        """Перезапись файла с добавлением самолета"""
        with open(self.filename, "r", encoding="utf-8") as loaded_file:
            data = json.load(loaded_file)

        airplane_dict = airplane.__dict__ if hasattr(airplane, "__dict__") else airplane
        data.append(airplane_dict)

        with open(self.filename, "w", encoding="utf-8") as result_file:
            json.dump(data, result_file, indent=4, ensure_ascii=False)

    def get_data(self, criteria=None):
        """Получение данных о самолетах по критерию и десериализация полученных словарей в список"""
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not criteria:
            return data
        else:
            result = [airplane for airplane in data if all(airplane.get(k) == v for k, v in criteria.items())]
            return result

    def delete_info(self, icao):
        """Удаление самолета по идентификатору ICAO"""
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        result = []
        for airplane in data:
            if airplane.get("icao") != icao:
                result.append(airplane)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    def clear_all(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    storage = JsonAirplaneStorage("test_airplanes.json")

    # 1. Очистим файл перед тестом
    storage.clear_all()

    # 2. Добавим пару самолетов (имитируем объекты через словари)
    plane1 = {"icao": "a8069d", "callsign": "CGCWD", "registration": "Canada"}
    plane2 = {"icao": "a53edd", "callsign": "GPD437", "registration": "USA"}

    storage.add_info(plane1)
    storage.add_info(plane2)
    print("Данные добавлены.")

    # 3. Проверим get_data без критериев
    all_planes = storage.get_data()
    print(f"Всего в базе: {len(all_planes)} самолета(ов).")

    # 4. Проверим фильтрацию по критерию
    search_criteria = {"callsign": "CGCWD"}
    found = storage.get_data(search_criteria)
    print(f"Найдено по позывному CGCWD: {found}")

    # 5. Проверим удаление
    storage.delete_info("a8069d")
    remaining = storage.get_data()
    print(f"Осталось после удаления: {len(remaining)} (должен быть 1)")

    # 6. Финальная очистка
    storage.clear_all()
