import pandas as pd
from excel import process_excel_input
from int_extractor import extract_int
from misc import announce_cleaning_result, announce_db_insert_result
from db import save_to_database


def get_filename_without_ext(filename):
    return ''.join(filename.split('.')[:-1])


def get_checked_filename():
    return filename_convoy_data if filename_convoy_data.endswith('[CHECKED].csv') \
        else get_filename_without_ext(filename_convoy_data) + '[CHECKED].csv'


class ReplacementCounter:
    checked = 0


def import_and_clean():
    initial_data = pd.read_csv(csv_filename)

    clean_data = initial_data.applymap(lambda x: extract_int(x, fix_counter))
    clean_data.set_index('vehicle_id', inplace=True)
    clean_data.to_csv(filename_checked_csv)

    announce_cleaning_result(fix_counter.checked, filename_checked_csv)


filename_convoy_data = input('Input file name\n')

fix_counter = ReplacementCounter()

csv_filename = get_filename_without_ext(filename_convoy_data) + '.csv'


# Omitting a lot of sanity checks to save time :)
if filename_convoy_data.endswith('.xlsx'):
    process_excel_input(filename_convoy_data, csv_filename)
elif filename_convoy_data.endswith('.csv'):
    pass
else:
    print('Invalid input!')
    raise SystemExit(0)


filename_checked_csv = get_checked_filename()

if not filename_convoy_data.endswith('[CHECKED].csv'):
    import_and_clean()


data_ready_for_db = pd.read_csv(filename_checked_csv)
table_name = 'convoy'
db_filename = filename_checked_csv.removesuffix('[CHECKED].csv') + '.s3db'

db_result = save_to_database(db_filename, table_name, data_ready_for_db)

announce_db_insert_result(db_result.records_inserted, db_filename)
