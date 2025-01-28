
import json
from dataclasses import dataclass


class JsonFile:

    def __init__(self, file_path: str)-> None:
        """
        Конструкторр класса JsonFile
        :param file_path: путь к файлу
        """
        self.file_path = file_path

    def read_data(self)-> list:
        """
        Метод для чтения данных из JSON файла
        :return: данные из файла
        """

        try:
            with open(self.file_path, "r", encoding = "utf-8") as file:
                data = json.load(file)
            return data
        except Exception as ex:
            print(ex)
            return []
        
    def write_data(self, data: list)-> None:
        """
        Метод для записи данных в JSON файл
        :param data: данные для записи
        :return: None
        """

        try:
            with open(self.file_path, "w", encoding = "utf-8") as file:
                json.dump(data, file, ensure_ascii = False)
        except Exception as ex:
            print(ex)

@dataclass
class City:
    """
    Датакласс для хранения списка городов
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float
    is_used: bool = False

class CitiesSerializer:
    def __init__(self, city_data: list[dict]) -> None:
        """
        Конструктор класса CitiesSerializer. Преобразует список словарей в список объектов класса City
        :param city_data: список словарей с данными о городах
        """
        self.cities = []
        for city in city_data:
            city_obj = City(
                name=city['name'],
                population=city['population'],
                subject=city['subject'],
                district=city['district'],
                latitude=float(city['coords']['lat']),
                longitude=float(city['coords']['lon']),
                is_used=False
            )
            self.cities.append(city_obj)
    
    def get_all_cities(self) -> list[City]:
        """
        Метод, возвращающий список всех городов
        :return: список объектов класса City
        """
        return self.cities
    
class CityGame:

    def __init__(self, cities: CitiesSerializer)-> None:
        self.cities = cities
        self.used_cities = []

    def start_game(self)-> None:
        """
        Метод для запуска игры
        """
        pass

    def human_turn(city_input):
        pass

    def computer_turn(self):
        pass

    def check_game_over(self):
        pass

    def save_game_state(self):
        pass


class GameManager(JsonFile, CitiesSerializer, CityGame):

    def __call__():
        pass

    def run_game(self):
        pass

    def display_game_result():
        pass