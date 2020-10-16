from abc import ABC, abstractmethod
import csv
from converter import MpsItem, TildaItem, WooItem


class ParserAbstract(ABC):
    COLUMN_ERROR = 'Сообщение об ошибке'

    def __init__(self):
        self.items = []
        self.index_by_sku = {}
        self.failed_rows = []

    def parse(self, filepath):
        with open(filepath, encoding='UTF-8') as csv_file:
            # fieldnames = csv_file.readline().split(',')
            csv_reader = csv.DictReader(csv_file)
            counter = 0
            for row in csv_reader:
                item = self.receive_item(row)
                if item:
                    self.items.append(item)
                    self.index_by_sku[item.sku] = counter
                    counter += 1

    @abstractmethod
    def receive_item(self, row):
        pass

    def get_by_sku(self, sku):
        return self.items[self.index_by_sku[sku]] if sku in self.index_by_sku.keys() else False


class TildaParser(ParserAbstract):
    def __init__(self, filepath):
        super().__init__()
        self.parse(filepath)

    def receive_item(self, row):
        validated = TildaItem.validate_row(row)
        if isinstance(validated, bool) and validated:
            return TildaItem.create_from_row(row)
        elif isinstance(validated, str):
            row[ParserAbstract.COLUMN_ERROR] = validated
            self.failed_rows.append(row)
            return False
        else:
            return False


class MpsParser(ParserAbstract):
    def __init__(self, filepath):
        super().__init__()
        self.parse(filepath)

    def receive_item(self, row):
        validated = MpsItem.validate_row(row)
        if isinstance(validated, bool) and validated:
            return MpsItem.create_from_row(row)
        elif isinstance(validated, str):
            row[ParserAbstract.COLUMN_ERROR] = validated
            self.failed_rows.append(row)
            return False
        else:
            return False


class WooParser(ParserAbstract):
    def __init__(self, filepath):
        super().__init__()
        self.parse(filepath)

    def receive_item(self, row):
        validated = WooItem.validate_row(row)
        if isinstance(validated, bool) and validated:
            return WooItem.create_from_row(row)
        elif isinstance(validated, str):
            row[ParserAbstract.COLUMN_ERROR] = validated
            self.failed_rows.append(row)
            return False
        else:
            return False
