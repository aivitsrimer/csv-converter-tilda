import csv
from converter import MpsItem, TildaItem, WooItem

COLUMN_UID = "Tilda UID"
COLUMN_SKU = "SKU"
COLUMN_CATEGORY = "Category"
COLUMN_TITLE = "Title"
COLUMN_PRICE = "Price"
COLUMN_QUANTITY = "Quantity"


class CsvBuilderAbstract:
    @staticmethod
    def build_and_write(items, out_dir):
        pass

    @staticmethod
    def _write_csv(filename, fieldnames, items):
        with open(filename, mode='w', encoding='UTF-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for item in items:
                writer.writerow(item)


class InsertCsvBuilder(CsvBuilderAbstract):
    DEFAULT_CATEGORY = 'import'
    DEFAULT_BRAND = 'Tegor'

    @staticmethod
    def build_and_write(items, out_dir):
        # type: (list[WooItem], str) -> None
        result = []
        for item in items:
            result.append({
                TildaItem.COLUMN_SKU: item.sku,
                TildaItem.COLUMN_BRAND: InsertCsvBuilder.DEFAULT_BRAND,
                TildaItem.COLUMN_CATEGORY: InsertCsvBuilder.DEFAULT_CATEGORY,
                TildaItem.COLUMN_TITLE: item.title,
                TildaItem.COLUMN_PRICE: float(item.price),
                TildaItem.COLUMN_QUANTITY: int(float(item.quantity)),
                TildaItem.COLUMN_DESCRIPTION: item.description,
                TildaItem.COLUMN_TEXT: item.description,
                TildaItem.COLUMN_PHOTO: item.image,
            })

        fieldnames = [
            TildaItem.COLUMN_SKU,
            TildaItem.COLUMN_CATEGORY,
            TildaItem.COLUMN_BRAND,
            TildaItem.COLUMN_TITLE,
            TildaItem.COLUMN_PRICE,
            TildaItem.COLUMN_QUANTITY,
            TildaItem.COLUMN_PHOTO,
            TildaItem.COLUMN_DESCRIPTION,
            TildaItem.COLUMN_TEXT,
        ]
        InsertCsvBuilder._write_csv(out_dir.rstrip('/') + '/insert.csv', fieldnames, result)


class UpdateCsvBuilder(CsvBuilderAbstract):
    @staticmethod
    def build_and_write(items, out_dir):
        # type: (list[TildaItem], str) -> None
        result = []
        for item in items:
            result.append({
                TildaItem.COLUMN_UID: item.tildaUID,
                TildaItem.COLUMN_PRICE: float(item.price),
                TildaItem.COLUMN_QUANTITY: int(float(item.quantity)),
            })

        fieldnames = [
            TildaItem.COLUMN_UID,
            TildaItem.COLUMN_PRICE,
            TildaItem.COLUMN_QUANTITY,
        ]
        UpdateCsvBuilder._write_csv(out_dir.rstrip('/') + '/update.csv', fieldnames, result)


class FailedCsvBuilder(CsvBuilderAbstract):
    prefix = ''

    @staticmethod
    def build_and_write(items, out_dir):
        # type: (list[dict], str) -> None
        fieldnames = []
        for item in items:
            fieldnames = item.keys()
        filename = out_dir.rstrip('/') + '/' + FailedCsvBuilder.prefix + '_failed.csv'
        UpdateCsvBuilder._write_csv(filename, fieldnames, items)
