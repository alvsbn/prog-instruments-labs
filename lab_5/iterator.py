import csv

class Iterator:
    def __init__(self, csv_file: str) -> None:
        self.csv_file = csv_file
        self.path_list = self.__read_csv()
        self.limit = len(self.path_list)
        self.counter = 0

    def __iter__(self) -> 'Iterator':
        return self

    def __next__(self):
        if self.counter < self.limit:
            next_element = self.path_list[self.counter]
            self.counter += 1
            return next_element
        else:
            raise StopIteration

    def __read_csv(self) -> list:
        with open(self.csv_file, mode='r', encoding = 'utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            path_list = []
            for row in reader:
                path_list.append(row[1])
            return path_list