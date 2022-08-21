import pandas as pd
from excel import process_excel_input
from int_extractor import extract_int
from misc import announce_result


def get_filename_without_ext(filename):
    return ''.join(filename.split('.')[:-1])


class ReplacementCounter:
    checked = 0


filename_convoy_data = input('Input file name\n')

fix_counter = ReplacementCounter()

csv_filename = get_filename_without_ext(filename_convoy_data) + '.csv'
filename_checked_csv = get_filename_without_ext(filename_convoy_data) + '[CHECKED].csv'

# Omitting a lot of sanity checks to save time :)
if filename_convoy_data.endswith('.xlsx'):
    process_excel_input(filename_convoy_data, csv_filename)
elif filename_convoy_data.endswith('.csv'):
    pass
else:
    print('Invalid input!')
    raise SystemExit(0)

initial_data = pd.read_csv(csv_filename)

clean_data = initial_data.applymap(lambda x: extract_int(x, fix_counter))
clean_data.set_index('vehicle_id', inplace=True)
clean_data.to_csv(filename_checked_csv)

announce_result(fix_counter, filename_checked_csv)
