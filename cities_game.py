
"""
Логика работы программы
1. Запуск
2. Чтение JSON файла со списком городов
3. Преобразование данных из файла в список объектов класса City
4. Создание списка плохих букв
5. Начало игры. Пусть компьютер ходит всегда первым.
6. Игрок выбирает первую букву.
    6.1 Проверка - буква дложна быть кириллической буквой.
    6.2 Буква не должна быть плохой
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
9. Повторение шагов 7-8 пока игрок не ошибётся или у компьютера не закончатся города.
10. Вывод сообщения о длительности игры.

Мораль сей басни - не делайте в ООП на 200 строк то что скриптом занимает 50.
"""




import json
from dataclasses import dataclass


class JsonFile:
    """
    Класс для работы с JSON файлами
    """

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
    """
    Класс для сериализации списка городов, полученного из JSON файла, в множество строк (названий городов).
    """
    def __init__(self, city_data: list[dict]) -> None:
        """
        Конструктор класса CitiesSerializer. Преобразует список словарей в сет строк (названий городов) и сохраняет их в атрибут класса.
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
        return self.cities
    
class CityGame:
    """
    Класс, управляющий логикой игры.
    """
    def __init__(self)-> None:
        """
        Конструктор класса CityGame
        :param alphabet: строка с алфавитом
        :param cities_set: сет имён городов
        :param bad_letters: сет букв, с которых не начинаются города
        :param iter: счётчик ходов
        """
        self.alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.cities_set = self.get_all_cities()
        self.bad_letters = self.make_bad_letter_set()
        self.iter = 0
        

    def start_game(self)-> None:
        """
        Метод для запуска игры. Реализует ввод и проверку первой буквы и запускает игровой цикл.
        """

        letter = input("Добро пожаловать в игру Города. Введите первую букву: ")
        if letter.lower() in self.alphabet:

            while letter in self.bad_letters:
                letter = input("Нет городов на эту букву! Введите первую букву: ")
            self.game_loop(letter)
        else:
            print("Некорректный ввод. Введите букву.")
            self.start_game()
        
    def human_turn(self, letter: str)-> str:
        """
        Метод для обработки хода игрока. Проверяет ввод игрока на корректность и возвращает букву, с которой должен начинаться следующий город.
        :param letter: буква, с которой начинается город
        :return letter: буква, с которой должен начинаться следующий городА
        """
        self.iter += 1
        user_input = input("Введите город: ")
        if self.check_game_over(user_input, letter):
            letter = user_input[-2] if user_input[-1] in self.bad_letters else user_input[-1]
            self.cities_set.remove(user_input.lower())

            return letter
        return ""    

    def computer_turn(self, letter: str)-> str:
        """
        Метод для обработки хода компьютера. Выбирает случайный город из списка городов, начинающийся на букву, которой кончается город игрока или для первого хода - букву которую ввёл игрок.
        :param letter: буква, с которой начинается город
        :return letter: буква, с которой должен начинаться следующий город
        """
        self.iter += 1
        for city in self.cities_set:
            if city[0].lower() == letter.lower():
                
                letter = city[-2] if city[-1] in self.bad_letters else city[-1]
                print(f"Компьютер выбрал город {city.capitalize()}. Вам на {letter}")
                self.cities_set.remove(city)
                return letter
                
        
        print("Нет городов на эту букву. Компьютер проиграл.")
        return ""
        

    def check_game_over(self, user_input: str, letter: str) -> bool:
        """
        Метод проверки корректности хода игрока. Проверяет, что введённый город начинается на букву, которой кончается предыдущий город и что город ещё не был использован.
        :param user_input: введённый игроком город
        :param letter: буква, с которой начинается город
        :return: True, если ход корректен, и False в противном случае
        """
        if user_input[0].lower() != letter.lower():
            print("Город начинается не на ту букву. Вы проиграли.")
            return False
        elif user_input.lower() not in self.cities_set:
            print("Такого города нет или он уже использован. Вы проиграли.")
            return False
        else:
            return True

    def game_loop(self, letter: str)-> None:
        """
        Метод, реализующий игровой цикл. Вызывает методы для хода игрока и компьютера, пока кто-либо не проиграет.
        :param letter: буква, с которой начинается город
        """

        while True:
            letter = self.computer_turn(letter)
            if not letter:
                break
            letter = self.human_turn(letter)
            if not letter:
                break

    def make_bad_letter_set(self)-> set:
        """
        Метод, создающий сет недопустимых букв.
        :return bad_letters: сет недопустимых букв
        """
        
        bad_letters = set(self.alphabet)

        for city in self.cities_set:
            if city[0].lower() in bad_letters:
                bad_letters.remove(city[0].lower())
        print(f"Недопустимые буквы: {bad_letters}")
        # print(len(bad_letters))
        # print(len(alphabet))
        return bad_letters


class GameManager(JsonFile, CitiesSerializer, CityGame):
    """
    Фасад для управления игрой. Дочерний класс от JsonFile, CitiesSerializer и CityGame.
    """

    def __init__(self, file_path: str = "cities.json")-> None:
        """
        Конструктор класса GameManager. Связывает классы JsonFile, CitiesSerializer и CityGame.
        :param file_path: путь к файлу с городами, по умолчанию cities.json
        """
        JsonFile.__init__(self, file_path)
        self.cities_data = self.read_data()
        CitiesSerializer.__init__(self, self.cities_data)
        CityGame.__init__(self)
     
    def __call__(self) -> None:
        """
        Дандер метод для запуска игры. Вызывает методы для запуска игры и вывода результата.
        """
        self.start_game()
        self.display_game_result()

    def display_game_result(self)-> None:
        """
        Метод для вывода результата игры. Выводит количество ходов, которое потребовалось для победы.
        """
        print(f"Игра закончена на {self.iter} ходу.")

def main():
    game = GameManager("cities.json")
    game()  

if __name__ == "__main__":
    main()