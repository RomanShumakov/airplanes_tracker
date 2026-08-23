import json
import os
from abc import ABC, abstractmethod


class AirplanesStorage(ABC):

    @abstractmethod
    def add_info(self, airplane):
        pass

    def get_data(self, criteria=None):
        pass

    @abstractmethod
    def delete_info(self):
        pass


class JsonAirplaneStorage(AirplanesStorage):
    """Класс для операций с самолетами в json-файле"""

    def __init__(self, filename="airplanes.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as new_file:
                json.dump([], new_file)

        def add_info(airplane):
            """Перезапись файла с добавлением самолета"""
            with open(self.filename, "r", encoding="utf-8") as loaded_file:
                data = json.load(loaded_file)
                data.append(airplane.__dict__)

            with open(self.filename, "w", encoding="utf-8") as result_file:
                json.dump(data, result_file, indent=4, ensure_ascii=False)

        def get_data(criteria=None):
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

        def delete_info(icao, callsign=None):
            """Удаление самолета по идентификатору ICAO или позывному callsign"""
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            result = []

            for airpalne in data:
                if airpalne.get("states")[0] != icao or airpalne.get("states")[1] != callsign:
                    result.append(airpalne)

            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

