
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

class CitiesSerializer:
    pass