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
                    print(f"{Color.Red}[!]{Color.Reset} Некорректный тип файла, используйте .csv или .xml.")
            else:
                query = input(f"{Color.Red}[!]{Color.Reset} Файл не найден. "
                              f"{Color.Yellow}[?]{Color.Reset} Попробовать снова? (y/n): ")
                if query.lower() == 'y':
                    continue
                elif query.lower() == 'n':
                    return None
                else:
                    print(f"{Color.Red}[!]{Color.Reset} Неверный ввод. Повторите попытку.")


class DataProcessor:
    """Класс для обработки данных."""

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
            next(f)  # Пропустить заголовок
            reader = csv.reader(f, delimiter=";", quotechar='"')
            for row in reader:
                row_tuple = tuple(row)
                self.uniq_rows[row_tuple] = self.uniq_rows.setdefault(row_tuple, 0) + 1

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
                self.uniq_rows[row_tuple] = self.uniq_rows.setdefault(row_tuple, 0) + 1

    def calculate_count_of_houses(self):
        for row in self.uniq_rows:
            key = (row[0], row[3])  # Город и количество этажей
            self.count_of_houses[key] = self.count_of_houses.setdefault(key, 0) + 1
        self.count_of_houses = dict(sorted(self.count_of_houses.items()))


class DataPresenter:
    """Класс для вывода информации."""

    @staticmethod
    def display_duplicates(uniq_rows):
        print(f"\n{Color.Green}[O]{Color.Blue} Дубликаты:{Color.Reset}\n")
        duplicates_found = False
        headers = ["Город", "Улица", "Дом", "Этажи", "Дубликаты"]
        max_lengths = [len(header) for header in headers]

        for k, v in uniq_rows.items():
            if v > 1:
                duplicates_found = True
                for i, item in enumerate(k):
                    max_lengths[i] = max(max_lengths[i], len(item))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        for k, v in uniq_rows.items():
            if v > 1:
                print("\t".join(str(k[i]).ljust(max_lengths[i]) for i in range(len(k))), f"\t{v}")

        if not duplicates_found:
            print(f"{Color.Red}[!] Дубликаты не найдены{Color.Reset}")

    @staticmethod
    def display_count_of_houses(count_of_houses):
        print(f"\n{Color.Green}[O]{Color.Blue} Количество домов в каждом городе:{Color.Reset}\n")
        headers = ["Город", "Этажи", "Дома"]
        max_lengths = [len(header) for header in headers]

        for (city, floors), count in count_of_houses.items():
            max_lengths[0] = max(max_lengths[0], len(city))
            max_lengths[1] = max(max_lengths[1], len(str(floors)))
            max_lengths[2] = max(max_lengths[2], len(str(count)))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        for (city, floors), count in count_of_houses.items():
            print(f"{city.ljust(max_lengths[0])}\t{str(floors).ljust(max_lengths[1])}\t{str(count).ljust(max_lengths[2])}")


class AppController:
    """Класс для управления приложением."""

    def __init__(self):
        self.file_handler = FileHandler()
        self.data_processor = None
        self.data_presenter = DataPresenter()

    def run(self):
        while True:
            path = self.file_handler.get_path()
            if path:
                start_time = time.time()

                self.data_processor = DataProcessor(path)
                self.data_processor.load_data()
                self.data_processor.calculate_count_of_houses()

                self.data_presenter.display_duplicates(self.data_processor.uniq_rows)
                self.data_presenter.display_count_of_houses(self.data_processor.count_of_houses)

                end_time = time.time()
                print(f"{Color.Green}[*]{Color.Reset} Время выполнения: {round(end_time - start_time, 2)} сек.\n")

                query = input(f"{Color.Yellow}[?]{Color.Reset} Продолжить? (y/n): ")
                if query.lower() != 'y':
                    break
            else:
                break


if __name__ == '__main__':
    app = AppController()
    app.run()
