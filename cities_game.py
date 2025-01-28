
"""
Логика работы программы
1. Запуск
2. Чтение JSON файла со списком городов
3. Преобразование данных из файла в список объектов класса City
4. Создание списка плохих букв
5. Начало игры. Пусть компьютер ходит всегда первым.
6. Игрок выбирает первую букву.
    6.1 Буква не должна быть плохой
7. Ход компьютера
    7.1. Компьютер выбирает город на букву, указанную игроком или ту, на которую заканчивается предыдущий город.
    7.2. Если город не найден, то компьютер проиграл.
    7.3. Город исключается из списка городов.
    7.4. Проверка на случай если город кончается на плохую букву
    7.5. Сообщение игроку о переходе хода и букве, с которой должен начинаться следующий город.
8. Ход игрока.
    8.1. Игрок вводит город.
    8.2. Проверка на проигрыш в случае если город не найден в списке городов или уже использован.
    8.3. Проверка на проигрыш в случае если город начинается не на ту букву, на которую заканчивается предыдущий город.
    8.4. Определение последней буквы введенного города с учётом плохих букв.
    8.5. Город исключается из списка городов.
"""




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