import pytest
import os
import json
from src.utils import JsonAirplaneStorage

@pytest.fixture
def temp_storage(tmp_path):
    """Фикстура для создания временного хранилища"""
    test_file = tmp_path / "test_airplanes.json"
    return JsonAirplaneStorage(str(test_file))

def test_add_and_get_data(temp_storage):
    plane = {"icao": "abc123", "callsign": "TEST777", "registration": "TestCountry"}
    temp_storage.add_info(plane)

    data = temp_storage.get_data()
    assert len(data) == 1
    assert data[0]["icao"] == "abc123"

def test_get_data_with_criteria(temp_storage):
    plane1 = {"icao": "1", "callsign": "ALPHA"}
    plane2 = {"icao": "2", "callsign": "BRAVO"}
    temp_storage.add_info(plane1)
    temp_storage.add_info(plane2)

    result = temp_storage.get_data({"callsign": "ALPHA"})
    assert len(result) == 1
    assert result[0]["icao"] == "1"

def test_delete_info(temp_storage):
    plane = {"icao": "delete_me", "callsign": "BYE"}
    temp_storage.add_info(plane)

    temp_storage.delete_info("delete_me")
    data = temp_storage.get_data()
    assert len(data) == 0

def test_clear_all(temp_storage):
    temp_storage.add_info({"icao": "1"})
    temp_storage.add_info({"icao": "2"})

    temp_storage.clear_all()
    assert len(temp_storage.get_data()) == 0

def test_private_filename(temp_storage):
    """Проверка приватности filename"""
    with pytest.raises(AttributeError):
        print(temp_storage.__filename)
