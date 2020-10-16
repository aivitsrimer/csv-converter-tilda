from dataclasses import dataclass
from re import search, findall
from typing import Union


@dataclass
class MpsItem:
    sku: str
    title: str
    price: str
    quantity: str

    COLUMN_SKU = "Артикул"
    COLUMN_TITLE = "Наименование"
    COLUMN_PRICE = "Цена"
    COLUMN_QUANTITY = "Кол-во"
    VALIDATE_COLUMNS = [COLUMN_SKU, COLUMN_TITLE, COLUMN_PRICE, COLUMN_QUANTITY]
    ALLOW_SKU_PREFIX = []

    @staticmethod
    def validate_row(row) -> Union[str, bool]:
        errors = []
        for key in MpsItem.VALIDATE_COLUMNS:
            if not (key in row.keys()):
                errors.append('Отсутствуют нужные поля')

        if row[MpsItem.COLUMN_SKU] == '' and row[MpsItem.COLUMN_TITLE] == '' and row[MpsItem.COLUMN_PRICE] == '':
            return False

        if row[MpsItem.COLUMN_SKU] == '':
            errors.append('Пустой артикул')
        else:
            if search(r'[^a-zA-Z-0-9]', row[MpsItem.COLUMN_SKU]):
                errors.append('Некорректный артикул (должен содержать только англ. буквы, цифры и тире)')
            else:
                prefix = findall(r'^([A-Z]{2,})-', row[MpsItem.COLUMN_SKU])
                if len(prefix) == 0:
                    errors.append('Некорректный артикул (отсуствует префикс бренда)')
                elif len(prefix) > 0 and prefix[0] not in MpsItem.ALLOW_SKU_PREFIX:
                    errors.append('Некорректный артикул (не совпадает с разрешенным списком префиксов брендов)')

        if row[MpsItem.COLUMN_TITLE] == '':
            errors.append('Пустое наименование')
        else:
            if search(r'[ ]{2,}', row[MpsItem.COLUMN_TITLE]):
                errors.append('Некорректное наименование (двойные пробелы)')
            if search(r'(^ )|( $)', row[MpsItem.COLUMN_TITLE]):
                errors.append('Некорректное наименование (пробел в начале или конце строки)')

        if int(float(row[MpsItem.COLUMN_PRICE])) == 0:
            errors.append('Некорректная цена')
        if int(float(row[MpsItem.COLUMN_QUANTITY])) < 0:
            errors.append('Некорректное количество')

        if len(errors) > 0:
            return ', '.join(errors)
        return True

    @staticmethod
    def create_from_row(row: dict) -> 'MpsItem':
        values = [row[key] for key in MpsItem.VALIDATE_COLUMNS]
        return MpsItem(*values)


@dataclass
class TildaItem:
    tildaUID: str
    sku: str
    category: str
    title: str
    price: str
    quantity: str

    COLUMN_UID = "Tilda UID"
    COLUMN_SKU = "SKU"
    COLUMN_CATEGORY = "Category"
    COLUMN_TITLE = "Title"
    COLUMN_PRICE = "Price"
    COLUMN_QUANTITY = "Quantity"
    VALIDATE_COLUMNS = [COLUMN_UID, COLUMN_SKU, COLUMN_CATEGORY, COLUMN_TITLE, COLUMN_PRICE, COLUMN_QUANTITY]

    @staticmethod
    def validate_row(row: dict) -> Union[str, bool]:
        for key in TildaItem.VALIDATE_COLUMNS:
            if not (key in row.keys()):
                return 'Отсутствуют нужные поля'
        return True

    @staticmethod
    def create_from_row(row: dict) -> 'TildaItem':
        values = [row[key] for key in TildaItem.VALIDATE_COLUMNS]
        return TildaItem(*values)


@dataclass
class WooItem:
    sku: str
    title: str
    description: str
    quantity: str
    price: str
    category: str
    image: str

    COLUMN_SKU = "Артикул"
    COLUMN_TITLE = "Имя"
    COLUMN_DESCRIPTION = "Описание"
    COLUMN_QUANTITY = "Запасы"
    COLUMN_PRICE = "Базовая цена"
    COLUMN_CATEGORY = "Категории"
    COLUMN_IMAGE = "Изображения"
    VALIDATE_COLUMNS = [COLUMN_SKU, COLUMN_TITLE, COLUMN_DESCRIPTION, COLUMN_QUANTITY, COLUMN_PRICE, COLUMN_CATEGORY,
                        COLUMN_IMAGE]

    @staticmethod
    def validate_row(row: dict) -> Union[str, bool]:
        for key in WooItem.VALIDATE_COLUMNS:
            if not (key in row.keys()):
                return 'Отсутствуют нужные поля'
        return True

    @staticmethod
    def create_from_row(row: dict) -> 'WooItem':
        values = [row[key] for key in WooItem.VALIDATE_COLUMNS]
        return WooItem(*values)
