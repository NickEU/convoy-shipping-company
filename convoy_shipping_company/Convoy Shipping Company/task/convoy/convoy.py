import pandas as pd
from excel import process_excel_input
from int_extractor import extract_int
from misc import announce_cleaning_result, announce_db_insert_result
from db import save_to_sqlite


def get_filename_without_ext(filename):
    return ''.join(filename.split('.')[:-1])


def get_checked_filename(filename_convoy_data):
    return filename_convoy_data if filename_convoy_data.endswith('[CHECKED].csv') \
        else get_filename_without_ext(filename_convoy_data) + '[CHECKED].csv'


class ReplacementCounter:
    checked = 0


def import_and_clean(csv_filename, filename_checked_csv):
    fix_counter = ReplacementCounter()
    initial_data = pd.read_csv(csv_filename)

    clean_data = initial_data.applymap(lambda x: extract_int(x, fix_counter))
    clean_data.set_index('vehicle_id', inplace=True)
    clean_data.to_csv(filename_checked_csv)

    announce_cleaning_result(fix_counter.checked, filename_checked_csv)


def save_to_db(filename_checked_csv):
    data_ready_for_db = pd.read_csv(filename_checked_csv)
    table_name = 'convoy'
    db_filename = filename_checked_csv.removesuffix('[CHECKED].csv') + '.s3db'

    db_result = save_to_sqlite(db_filename, table_name, data_ready_for_db)

    announce_db_insert_result(db_result.records_inserted, db_filename)


def process_user_input(filename_user_input, filename_csv_target):
    # Omitting a lot of sanity checks to save time :)
    if filename_user_input.endswith('.xlsx'):
        process_excel_input(filename_user_input, filename_csv_target)
    elif filename_user_input.endswith('.csv'):
        pass
    else:
        print('Invalid input!')
        raise SystemExit(0)


def main_menu():
    filename_user_input = input('Input file name\n')

    filename_csv_target = get_filename_without_ext(filename_user_input) + '.csv'

    process_user_input(filename_user_input, filename_csv_target)

    filename_checked_csv = get_checked_filename(filename_user_input)

    if filename_user_input != filename_checked_csv:
        import_and_clean(filename_csv_target, filename_checked_csv)

    save_to_db(filename_checked_csv)


main_menu()
