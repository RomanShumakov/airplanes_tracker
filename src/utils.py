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
    def delete_info(self, icao, callsign=None):
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
            result = []
            for k, v in data.items():
                if data[k] == v:
                    result.append(f"{data[k]}: {v}")
            return result

    def delete_info(self, icao):
        """Удаление самолета по идентификатору ICAO или позывному callsign"""
        with open(self.filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        result = []
        for airpalne in data:
            if airpalne.get("icao") != icao:
                result.append(airpalne)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    def clear_all(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    if __name__ == "__main__":
        storage = JsonAirplaneStorage("test_airplanes.json")

        test_plane = {
            "icao24": "a8069d",
            "callsign": "CGCWD ",
            "origin_country": "Canada",
            "velocity": 210.5
        }

        print("Сохраняем тестовый самолет...")
        storage.add_info(test_plane)

        data = storage.get_data()
        print(f"Данные из файла: {data}")

        result = storage.get_data(criteria={"icao24": "a8069d"})
        print(f"Результат поиска по ICAO: {result}")

        print("Удаляем данные...")
        storage.delete_info(icao="a8069d")

        final_data = storage.get_data()
        print(f"Файл после удаления: {final_data}")

