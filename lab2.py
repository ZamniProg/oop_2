import csv
import os
import time


class Color:
    Reset = '\033[0m'

    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'


class GetInfo:
    def __init__(self):
        self.path = self.get_path()
        self.count_of_houses = dict()
        self.uniq_rows = dict()

    @staticmethod
    def get_path():
        while True:
            path_to_csv_file = input("{}[*]{} Введите путь до файла: ".format(Color.Green, Color.Reset))

            if os.path.exists(path_to_csv_file):
                return path_to_csv_file
            else:
                query = input("{}[!]{} К сожалению файл не был обнаружен по указанному пути\n"
                              "{}[?]{} Вы хотите продолжить поиск?(y/n): ".format(Color.Red,
                                                                                  Color.Reset,
                                                                                  Color.Yellow,
                                                                                  Color.Reset))
                if query == 'y':
                    continue
                elif query == 'n':
                    return None
                else:
                    print("{}[!]{} К сожалению, вы ввели неверный символ, "
                          "поэтому вам снова будет предложено ввести путь до файла!".format(Color.Red, Color.Reset))

    def get_count_of_houses(self):
        if self.uniq_rows is not None:
            for k in self.uniq_rows:
                key = (k[0], k[3])
                self.count_of_houses[key] = self.count_of_houses.setdefault(key, 0) + 1
        self.count_of_houses = dict(sorted(self.count_of_houses.items()))

    def uniq(self):
        if self.path is not None:
            with open(self.path, 'r', encoding="utf-8") as f:
                next(f)
                spam_reader = csv.reader(f, delimiter=";", quotechar='"')

                for row in spam_reader:
                    row_tuple = tuple(row)
                    self.uniq_rows[row_tuple] = self.uniq_rows.setdefault(row_tuple, 0) + 1

    def out_duplicates(self):
        print("\n{}[O]{} Дубликаты: {}\n".format(Color.Green, Color.Blue, Color.Reset))
        duplicates_found = False
        headers = ["Город", "Улица", "Номер дома", "Количество этажей", "Количество дубликатов"]

        max_lengths = [len(header) for header in headers]

        for k, v in self.uniq_rows.items():
            if v > 1:
                duplicates_found = True
                for i, item in enumerate(k):
                    max_lengths[i] = max(max_lengths[i], len(item))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        for k, v in self.uniq_rows.items():
            if v > 1:
                print(f"{(max_lengths[0] + 4) * "-"}"
                      f"{(max_lengths[1] + 4) * "-"}"
                      f"{(max_lengths[2] + 4) * "-"}"
                      f"{(max_lengths[3] + 4) * "-"}"
                      f"{max_lengths[4] * "-"}")
                print("\t".join(str(k[i]).ljust(max_lengths[i]) for i in range(len(k))), f"\t{v}")

        if not duplicates_found:
            print("Дубликаты не были найдены")

        print("\n")

    def out_count_of_houses(self):
        print("{}[O]{} Количество домов в каждом городе по этажам: {}\n".format(Color.Green, Color.Blue, Color.Reset))
        headers = ["Город", "Количество этажей", "Количество домов"]

        max_lengths = [len(header) for header in headers]

        for (city, floors), count in self.count_of_houses.items():
            max_lengths[0] = max(max_lengths[0], len(city))
            max_lengths[1] = max(max_lengths[1], len(str(floors)))
            max_lengths[2] = max(max_lengths[2], len(str(count)))

        header_row = "\t".join(header.ljust(max_lengths[i]) for i, header in enumerate(headers))
        print(header_row)

        prev_city = ""

        for (city, floors), count in self.count_of_houses.items():
            if city != prev_city:
                print(f"{(max_lengths[0] + 4) * "-"}"
                      f"{(max_lengths[1] + 4) * "-"}"
                      f"{max_lengths[2] * "-"}")
            if int(floors) == 3:
                print(f"{str(city.ljust(max_lengths[0]))}\t"
                      f"{str(floors).ljust(max_lengths[1])}\t"
                      f"{str(count).ljust(max_lengths[2])}")
            else:
                print(f"{''.ljust(max_lengths[0])}\t"
                      f"{str(floors).ljust(max_lengths[1])}\t"
                      f"{str(count).ljust(max_lengths[2])}")
            prev_city = city

        print(f"{(max_lengths[0] + 4) * "-"}"
              f"{(max_lengths[1] + 4) * "-"}"
              f"{max_lengths[2] * "-"}\n")


def process():
    r = 1

    while r:
        proc = GetInfo()

        if proc.path:
            start_time = time.time()

            proc.uniq()
            proc.get_count_of_houses()
            proc.out_duplicates()
            proc.out_count_of_houses()

            end_time = time.time()
            print("{}[*]{} Время выполнения программы: ".format(Color.Green, Color.Reset),
                  round(end_time - start_time, 5), "сек.\n")

            while True:
                r = input("{}[?]{} Продолжить (y/n)? ".format(Color.Yellow, Color.Reset))
                if r.lower() == 'y':
                    r = 1
                    break
                elif r.lower() == 'n':
                    r = 0
                    break
                else:
                    print("{}[!]{} Некорректный ввод. Введите 'y' или 'n'.".format(Color.Red, Color.Reset))
        else:
            break


if __name__ == '__main__':
    process()
