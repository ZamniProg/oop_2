import csv
import os
import xml.etree.ElementTree as ET
import time


class Color:
    Reset = '\033[0m'
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'


class FileHandler:
    """Класс для работы с файлами."""

    @staticmethod
    def get_path():
        while True:
            path_to_file = input(f"{Color.Green}[*]{Color.Reset} Введите путь до файла: ")

            if os.path.exists(path_to_file):
                if path_to_file.endswith('.csv') or path_to_file.endswith('.xml'):
                    return path_to_file
                else:
                    print(f"{Color.Red}[!]{Color.Reset} Введен неверный тип файла. "
                          f"Пожалуйста, используйте XML или CSV.")
            else:
                if len(path_to_file) == 0:
                    print(f"{Color.Red}[!]{Color.Reset} Не вводите пустую строку.")
                    continue
                query = input(f"{Color.Red}[!]{Color.Reset} Файл не найден.\n"
                              f"{Color.Yellow}[?]{Color.Reset} Хотите продолжить поиск? (y/n): ")
                if query.lower() == 'y':
                    continue
                elif query.lower() == 'n':
                    return None
                else:
                    print(f"{Color.Red}[!]{Color.Reset} Неверный ввод. Попробуйте снова!")


class DataProcessor:
    """Класс для обработки данных из файла."""

    def __init__(self, path):
        self.path = path
        self.uniq_rows = {}
        self.count_of_houses = {}

    def load_data(self):
        if self.path.endswith(".csv"):
            self._process_csv()
        elif self.path.endswith(".xml"):
            self._process_xml()

    def _process_csv(self):
        with open(self.path, 'r', encoding="utf-8") as f:
            next(f)
            reader = csv.reader(f, delimiter=";", quotechar='"')
            for row in reader:
                row_tuple = tuple(row)
                self.uniq_rows[row_tuple] = self.uniq_rows.get(row_tuple, 0) + 1

    def _process_xml(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        for item in root.findall("item"):
            city = item.get('city')
            street = item.get('street')
            house = item.get('house')
            floor = item.get('floor')
            row_tuple = (city, street, house, floor)
            if all(row_tuple):
                self.uniq_rows[row_tuple] = self.uniq_rows.get(row_tuple, 0) + 1

    def calculate_house_counts(self):
        for row in self.uniq_rows:
            key = (row[0], row[3])  # (город, количество этажей)
            self.count_of_houses[key] = self.count_of_houses.get(key, 0) + 1
        self.count_of_houses = dict(sorted(self.count_of_houses.items()))


class DataPresenter:
    """Класс для отображения данных."""

    @staticmethod
    def display_duplicates(uniq_rows):
        print(f"\n{Color.Green}[O]{Color.Blue} Дубликаты: {Color.Reset}\n")
        headers = ["Город", "Улица", "Номер дома", "Количество этажей", "Количество дубликатов"]
        max_lengths = [len(header) for header in headers]

        for k, v in uniq_rows.items():
            if v > 1:
                for i, item in enumerate(k):
                    max_lengths[i] = max(max_lengths[i], len(item))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        for k, v in uniq_rows.items():
            if v > 1:
                print("-" * (sum(max_lengths) + 12))
                print("\t".join(str(k[i]).ljust(max_lengths[i]) for i in range(len(k))), f"\t{v}")

        if not any(v > 1 for v in uniq_rows.values()):
            print(f"{Color.Red}[!]{Color.Reset} Дубликаты не найдены.")

        print("\n")

    @staticmethod
    def display_house_counts(count_of_houses):
        print(f"{Color.Green}[O]{Color.Blue} Количество домов в каждом городе по этажам: {Color.Reset}\n")
        headers = ["Город", "Количество этажей", "Количество домов"]
        max_lengths = [len(header) for header in headers]

        for (city, floors), count in count_of_houses.items():
            max_lengths[0] = max(max_lengths[0], len(city))
            max_lengths[1] = max(max_lengths[1], len(str(floors)))
            max_lengths[2] = max(max_lengths[2], len(str(count)))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        prev_city = ""
        for (city, floors), count in count_of_houses.items():
            if city != prev_city:
                print("-" * (sum(max_lengths) + 12))
            if int(floors) == 3:
                print(f"{city.ljust(max_lengths[0])}\t"
                      f"{str(floors).ljust(max_lengths[1])}\t"
                      f"{str(count).ljust(max_lengths[2])}")
            else:
                print(f"{''.ljust(max_lengths[0])}\t"
                      f"{str(floors).ljust(max_lengths[1])}\t"
                      f"{str(count).ljust(max_lengths[2])}")
            prev_city = city

        print("-" * (sum(max_lengths) + 12))


class AppController:
    """Класс для управления процессом."""

    @staticmethod
    def run():
        while True:
            path = FileHandler.get_path()
            if not path:
                break

            start_time = time.time()
            processor = DataProcessor(path)
            processor.load_data()
            processor.calculate_house_counts()

            presenter = DataPresenter()
            presenter.display_duplicates(processor.uniq_rows)
            presenter.display_house_counts(processor.count_of_houses)

            end_time = time.time()
            print(f"{Color.Green}[*]{Color.Reset} Время выполнения программы: {round(end_time - start_time, 5)} сек.\n")

            while True:
                query = input(f"{Color.Yellow}[?]{Color.Reset} Продолжить (y/n)? ").lower()
                if query == 'y':
                    break
                elif query == 'n':
                    return
                else:
                    print(f"{Color.Red}[!]{Color.Reset} Неверный ввод. Введите 'y' или 'n'.")


if __name__ == '__main__':
    AppController().run()
