import pytest
from src.views import CountryCords, AirplanesCords, AirplanesAnalyzer

def test_county_cords_returns_list():
    """Проверяем получения координат на маленькой стране, чтобы координаты были стабильными"""
    country_service = CountryCords("https://nominatim.openstreetmap.org/search", "Monaco")
    coords = country_service.get_data()

    assert isinstance(coords, list)
    assert len(coords) == 4
    assert all(isinstance(c, str) for c in coords)


def test_airplane_analyzer_from_vector():
    """Имитация ответа от OpenSky (список данных об одном самолете)"""
    # state[0]=icao, state[1]=callsign, state[2]=origin_country, state[4]=time, state[7]=alt, state[9]=vel
    mock_vector = ["a4b3c2", "AFL123", "Russia", 1700000000, 1700000000, None, None, 10000, None, 250.5]

    airplane = AirplanesAnalyzer.from_opensky_vector(mock_vector)

    assert airplane.icao == "a4b3c2"
    assert airplane.velocity == 250.5
    assert airplane.altitude == 10000


def test_airplane_validation():
    airplane = AirplanesAnalyzer("icao123", "", "REG-999", 12345, 200, 5000)
    airplane.validation()

    assert airplane.callsign == "icao123_REG-999"


def test_airplane_comparison():
    """Проверка магических методов"""
    p1 = AirplanesAnalyzer("1", "FastHigh", "R1", 0, 500, 10000)
    p2 = AirplanesAnalyzer("2", "SlowLow", "R2", 0, 300, 5000)

    assert p1 > p2
    assert p2 < p1
    assert not (p1 <= p2)
