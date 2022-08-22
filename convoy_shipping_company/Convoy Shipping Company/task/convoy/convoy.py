import pandas as pd
from excel import process_excel_input
from int_extractor import extract_int
from misc import announce_cleaning_result, announce_db_insert_result, announce_file_save_result
from db import save_to_sqlite
import json_local
from db import get_rows_from_table
import xml_local


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


def save_to_db(filename_checked_csv, table_name):
    data_ready_for_db = pd.read_csv(filename_checked_csv)
    db_filename = filename_checked_csv.removesuffix('[CHECKED].csv') + '.s3db'

    db_result = save_to_sqlite(db_filename, table_name, data_ready_for_db)

    announce_db_insert_result(db_result.records_inserted, db_filename)
    return db_filename


def process_user_input(filename_user_input, filename_csv_target):
    # Omitting a lot of sanity checks to save time :)
    if filename_user_input.endswith('.xlsx'):
        process_excel_input(filename_user_input, filename_csv_target)
    elif filename_user_input.endswith(('.csv', '.s3db')):
        pass
    else:
        print('Invalid input!')
        raise SystemExit(0)


def save_to_json(rows, save_to_filename, table_name):
    vehicles_saved = json_local.save_to_json(rows, save_to_filename, table_name)
    announce_file_save_result(vehicles_saved, save_to_filename)


def save_to_xml(rows, save_to_filename, table_name):
    vehicles_saved = xml_local.save_to_xml(rows, save_to_filename, table_name, 'vehicle')
    announce_file_save_result(vehicles_saved, save_to_filename)


def main_menu():
    # filename_user_input = "data_final_xlsx.xlsx"
    filename_user_input = input('Input file name\n')
    filename_csv_target = get_filename_without_ext(filename_user_input) + '.csv'

    process_user_input(filename_user_input, filename_csv_target)

    filename_checked_csv = get_checked_filename(filename_user_input)
    table_name = 'convoy'
    # We have a valid and supported file
    if not filename_user_input.endswith('.s3db'):
        if filename_user_input != filename_checked_csv:
            # The input data is dirty, need to clean first
            import_and_clean(filename_csv_target, filename_checked_csv)
        db_filename = save_to_db(filename_checked_csv, table_name)
    else:
        db_filename = filename_user_input

    # If we got here the db file is guaranteed to exist, can export it to JSON/XML
    rows = get_rows_from_table(db_filename, table_name)
    filename_user_input = filename_user_input.replace('[CHECKED].csv', '.csv')
    save_to_json(rows, get_filename_without_ext(filename_user_input) + '.json', table_name)
    save_to_xml(rows, get_filename_without_ext(filename_user_input) + '.xml', table_name)


main_menu()
