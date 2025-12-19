import csv
import logging


logger = logging.getLogger(__name__)


class Iterator:
    def __init__(self, csv_file: str) -> None:
        self.csv_file = csv_file
        logger.info("Загрузка CSV файла: %s", csv_file)
        try:
            self.path_list = self.__read_csv()
            self.limit = len(self.path_list)
            self.counter = 0
            logger.info("Успешно загружено %d записей из файла", self.limit)
        except Exception as e:
            logger.error("Ошибка при загрузке файла %s: %s", csv_file, e, exc_info=True)
            raise

    def __iter__(self) -> 'Iterator':
        return self

    def __next__(self):
        if self.counter < self.limit:
            next_element = self.path_list[self.counter]
            logger.debug("Получение элемента %d: %s", self.counter, next_element)
            self.counter += 1
            return next_element
        else:
            logger.info("Достигнут конец данных итератора")
            raise StopIteration

    def __read_csv(self) -> list:
        logger.debug("Начало чтения CSV файла")
        try:
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                logger.debug("Пропущен заголовок CSV файла")

                path_list = []
                line_count = 1

                for row in reader:
                    line_count += 1
                    if len(row) > 1:
                        path_list.append(row[1])
                    else:
                        logger.warning("Строка %d не содержит второго столбца", line_count)

                logger.debug("Завершено чтение CSV, обработано %d строк", line_count)
                return path_list

        except FileNotFoundError:
            logger.error("Файл не найден: %s", self.csv_file)
            raise
        except Exception as e:
            logger.error("Ошибка при чтении CSV: %s", e, exc_info=True)
            raise