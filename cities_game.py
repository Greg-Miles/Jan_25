
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
        Конструктор класса CitiesSerializer. Преобразует список словарей в сет объектов класса City
        :param city_data: список словарей с данными о городах
        """
        self.cities = set()
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
            self.cities.add(city_obj.name.lower())
    
    def get_all_cities(self) -> set:
        """
        Метод, возвращающий сет всех городов
        :return: сет параметров name объектов класса City
        """
        # city_names = set()
        # for city in self.cities:
        #     city_names.add(city.name.lower())
        return self.cities
    
class CityGame:
     
    iter = 0

    def __init__(self, cities: CitiesSerializer)-> None:
        # self.cities = cities
        self.cities_set = self.get_all_cities()
        self.bad_letters = self.make_bad_letter_set()
        

    def start_game(self)-> None:
        """
        Метод для запуска игры
        """

        letter = input("Введите первую букву: ")
        while letter in self.bad_letters:
            letter = input("Введите первую букву: ")
        self.game_loop(letter)
        
    def human_turn(self, letter: str)-> str:
        self.iter += 1
        user_input = input("Введите город: ")
        if self.check_game_over(user_input, letter):
            letter = user_input[-2] if user_input[-1] in self.bad_letters else user_input[-1]
            self.city_set.remove(user_input.lower())
    

    def computer_turn(self, letter: str)-> str:

        self.iter += 1
        for city in self.cities_set:
            if city[0].lower() == letter.lower():
                
                letter = city[-2] if city[-1] in self.bad_letters else city[-1]
                print(f"Компьютер выбрал город {city}. Вам на {letter}")
                self.cities.get_all_cities().remove(city)
                return letter
                
            else:
                print("Нет городов на эту букву. Компьютер проиграл.")
                break
        

    def check_game_over(self, user_input: str, letter: str) -> bool:
        if user_input[0].lower() != letter.lower():
            print("Город начинается не на ту букву. Вы проиграли.")
            return False
        elif user_input.lower() not in self.city_set():
            print("Такого города нет или он уже использован. Вы проиграли.")
            return False
        else:
            return True

    def game_loop(self, letter: str)-> None:
        while True:
            letter = self.computer_turn(letter)
            if not letter:
                break
            letter = self.human_turn(letter)
            if not letter:
                break

    def make_bad_letter_set(self)-> set:
        bad_letters = set()
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

        for letter in alphabet:
            found = False
            for city in self.cities_set:
                first_letter = city[0]
                if letter.lower() == first_letter.lower():
                    found = True
                    break
            if not found:
                bad_letters.add(letter)
        return bad_letters


class GameManager(JsonFile, CitiesSerializer, CityGame):

    def __init__(self, file_path: str = "cities.json")-> None:
        JsonFile.__init__(self, file_path)
        self.cities_data = self.read_data()
        CitiesSerializer.__init__(self, self.cities_data)
        CityGame.__init__(self, self)
        


    def __call__(self, file_path: str = "cities.json") -> None:
        self.run_game()

    def run_game(self):
        self.start_game()
        self.display_game_result()

    def display_game_result(self)-> None:
        print(f"Игра закончена на {self.iter} ходу.")

def main():
    game = GameManager("cities.json")
    game()  # или game.run_game()

if __name__ == "__main__":
    main()