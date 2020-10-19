import sys
from converter import *
import re


def main(woo_filepath: str, out_dir: str):
    # tilda_csv = TildaParser(tilda_filepath)
    # print('Tilda csv parsed, len:', len(tilda_csv.index_by_sku))
    #
    # MpsItem.ALLOW_SKU_PREFIX = sku_prefixes.split(',')
    #
    # mps_csv = MpsParser(mps_filepath)
    # print('Mps csv parsed, len:', len(mps_csv.index_by_sku))

    woo_csv = WooParser(woo_filepath)
    print('Woo csv parsed, len:', len(woo_csv.index_by_sku))

    convert(woo_csv)

    InsertCsvBuilder.build_and_write(woo_csv.items, out_dir)
    print('csv for insert created')

    # new_items, update_items = compare(tilda_csv, mps_csv)
    #
    # if len(new_items) > 0:
    #     InsertCsvBuilder.build_and_write(new_items, out_dir)
    #     print('csv for insert created')
    # if len(update_items) > 0:
    #     UpdateCsvBuilder.build_and_write(update_items, out_dir)
    #     print('csv for update created')
    #
    # if len(tilda_csv.failed_rows) > 0:
    #     FailedCsvBuilder.prefix = 'tilda'
    #     FailedCsvBuilder.build_and_write(tilda_csv.failed_rows, out_dir)
    #     print('tilda export errors csv created')
    # if len(mps_csv.failed_rows) > 0:
    #     FailedCsvBuilder.prefix = 'mps'
    #     FailedCsvBuilder.build_and_write(mps_csv.failed_rows, out_dir)
    #     print('mps export errors csv created')
    #
    # if len(new_items) > 0 or len(update_items) > 0:
    #     print('Finished! all files in', out_dir)
    # else:
    #     print("Finished!")


def compare(tilda_csv: TildaParser, mps_csv: MpsParser) -> tuple:
    new_items = []
    update_items = []
    for mps_sku, mps_index in mps_csv.index_by_sku.items():
        tilda_item = tilda_csv.get_by_sku(mps_sku)
        mps_item: MpsItem = mps_csv.items[mps_index]
        if tilda_item:
            if float(mps_item.price) != float(tilda_item.price) \
                    or int(float(mps_item.quantity)) != int(float(tilda_item.quantity)):
                tilda_item.price = float(mps_item.price)
                tilda_item.quantity = int(float(mps_item.quantity))
                update_items.append(tilda_item)
        else:
            new_items.append(mps_item)
    return new_items, update_items


def convert(woo_csv: WooParser):
    item: WooItem
    for item in woo_csv.items:
        item.price = re.sub(r',', '.', item.price)
        item.description = re.sub(r'<b>', '<strong>', item.description)
        item.description = re.sub(r'</b>', '</strong>', item.description)
        item.description = re.sub(r'(((?!</?strong>))(<[^>]*?>))|(\\n)', '', item.description)
        item.description = re.sub(r'\n\n', '\n', item.description)
        item.description = item.description.strip('\n')
        item.description = re.sub(r'\n', '<br />', item.description)
        item.image = item.image.split(', ')[0]


def init():
    ARG_WOO_CSV = 'woo'
    ARG_OUT_DIR = 'out'
    ALLOW_ARGS = [ARG_WOO_CSV, ARG_OUT_DIR]
    args = {}
    for arg in sys.argv:
        split_arg = arg.split('=')
        if split_arg[0] in ALLOW_ARGS:
            args[split_arg[0]] = split_arg[1]
    if len(args) == len(ALLOW_ARGS):
        main(args[ARG_WOO_CSV], args[ARG_OUT_DIR])
    else:
        print("Doesn't set parameters:", *ALLOW_ARGS)


if __name__ == '__main__':
    init()
