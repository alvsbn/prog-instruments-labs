import csv
import re
from typing import List
from checksum import calculate_checksum, serialize_result


VARIANT = 66
CSV_FILE = "66.csv"
PATTERNS = {
    'telephone': r'^\+7\-\(\d{3}\)\-\d{3}\-\d{2}\-\d{2}$',
    'http_status_message': r'^\d{3}\s[A-Za-z\s\-]+$',
    'snils': r'^\d{11}$',
    'identifier': r'^[0-9]{2}\-[0-9]{2}\/[0-9]{2}$',
    'ip_v4': r'^(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)$',
    'longitude': r'^-?\d{1,3}\.\d+$',
    'blood_type': r'^(?:A|B|AB|O)[+\−]$',
    'isbn': r"^\d+-\d+-\d+-\d+(:?-\d+)?$",
    'locale_code': r'^[a-z]{2,3}(?:-[a-z]{2,3})?$',
    'date': r'^\d{4}-\d{2}-\d{2}$'
}


def read_csv(csv_file: str) -> list:
    """
    Читает CSV-файл
    :param csv_file: путь к файлу
    :return: список строк
    """
    with open(csv_file, 'r', encoding='utf-16') as file:
        reader = csv.DictReader(file, delimiter=';')
        data = []
        for element in reader:
            data.append(element)

    return data


def longitude(longitude_tmp: str) -> bool:
    """
        Проверка долготы на корректность
        :param longitude_tmp: значение долготы
        :return: true, если корректно, иначе false
    """
    value = float(longitude_tmp)
    return -180 <= value <= 180


def validate_row(row: dict) -> bool:
    """
    Проверяют строку на соответсвие шаблону
    :param row: данные
    :return: true, если корректно, иначе false
    """
    for field_name, value in row.items():
        if field_name not in PATTERNS:
            continue

        value = value.strip()
        if not re.match(PATTERNS[field_name], value):
            return False
        if field_name == 'longitude':
            if longitude(value) == False:
                return False
    return True


def search_invalid_rows(csv_file: str) -> List[int]:
    """
    Ищет некорректные строки в CSV файле
    :param csv_file: путь к файлу
    :return: список индексов некорректных строк
    """
    invalid_rows = []
    data = read_csv(csv_file)

    for row_num, row in enumerate(data):
        if not validate_row(row):
            invalid_rows.append(row_num)

    return invalid_rows


def main() -> None:
    invalid_rows = search_invalid_rows(CSV_FILE)
    checksum = calculate_checksum(invalid_rows)
    serialize_result(VARIANT, checksum)


if __name__ == "__main__":
    main()