from abc import ABC, abstractmethod
import requests
import json


class AbstractClass(ABC):

    @abstractmethod
    def get_data(self):
        pass


class AirplanesCords(AbstractClass):
    """Класс для получения данных о всех самолетах, выполняющих полет в прямоугольных координатам"""

    def __init__(self, opensky_url, sqrt_cords):
        self.opensky_url = opensky_url
        self.params_opensky = sqrt_cords
        self.headers_opensky = {
            'User-Agent': 'test-app/1.0',
        }

    def get_data(self):
        response = requests.get(url=self.opensky_url, params=self.params_opensky, headers=self.headers_opensky)
        return response.json()


class CountyCords(AbstractClass):
    """Класс для получения прямоугольных координат страны по ее названию"""

    def __init__(self, openstreetmap_url, country):
        self.openstreetmap_url = openstreetmap_url
        self.params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        self.headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }

    def get_data(self):
        response = requests.get(url=self.openstreetmap_url, params=self.params_nominatim,
                                headers=self.headers_nominatim)
        sqrt_cords_str = response.json()[0].get("boundingbox")
        return sqrt_cords_str


class AirplanesAnalyzer:
    """Класс для сравнения самолетов по скорости и высоте"""

    def __init__(self, icao, callsign, registration, time, velocity, altitude):
        self.icao = icao
        self.callsign = callsign
        self.registration = registration
        self.time = time
        self.velocity = velocity
        self.altitude = altitude

    @classmethod
    def from_opensky_vector(cls, state):
        """Создает объект AirplanesAnalyzer напрямую из списка состояния OpenSky"""

        return cls(
            icao=state[0],
            callsign=state[1],
            registration=state[2],
            time=state[4],
            velocity=state[9],
            altitude=state[7]
        )

    def validation(self):
        self.callsign = self.callsign if self.callsign else f"{self.icao}_{self.registration}"

    def __le__(self, other):
        return (self.velocity <= other.velocity) and (self.altitude <= other.altitude)

    def __lt__(self, other):
        return (self.velocity < other.velocity) and (self.altitude < other.altitude)

    def __gt__(self, other):
        return (self.velocity > other.velocity) and (self.altitude > other.altitude)

    def __ge__(self, other):
        return (self.velocity >= other.velocity) and (self.altitude >= other.altitude)

    def __repr__(self):
        return f"AirplanesAnalyzer(ICAO='{self.icao}', callsign='{self.callsign}', velocity={self.velocity})"


if __name__ == '__main__':
    countries = CountyCords("https://nominatim.openstreetmap.org/search", "Canada")
    country_cords = countries.get_data()
    # countries_data = json.dumps(countries_a, indent=4, ensure_ascii=False)

    params = {
        "lamin": float(country_cords[0]),
        "lamax": float(country_cords[1]),
        "lomin": float(country_cords[2]),
        "lomax": float(country_cords[3])
    }

    airplanes = AirplanesCords('https://opensky-network.org/api/states/all', params)
    airplanes_data = airplanes.get_data()
    airplanes_result = json.dumps(airplanes_data, indent=4, ensure_ascii=False)

    airplanes_list = []

    for s in airplanes_data['states']:
        new_plane = AirplanesAnalyzer.from_opensky_vector(s)
        airplanes_list.append(new_plane)
    print(airplanes_list)