import pandas as pd
import re


def get_filename_without_ext(filename):
    return ''.join(filename.split('.')[:-1])


def extract_int(to_sanitize):
    global checked
    matches = pattern.findall(str(to_sanitize))
    if str(matches[0]) != str(to_sanitize):
        checked += 1
    return to_sanitize if not matches else matches[0]


def print_excel_import_result(df_input):
    rows_imported = df_input.shape[0]
    lines_line = '' if rows_imported == 1 else 's'
    was_were = 'was' if rows_imported == 1 else 'were'
    print(f"{rows_imported} line{lines_line} {was_were} imported to {csv_filename}")


filename_convoy_data = input('Input file name\n')

regex_look_for_integers = r"\d+"
pattern = re.compile(regex_look_for_integers)
checked = 0

df = None
filename_checked_csv = get_filename_without_ext(filename_convoy_data) + '[CHECKED].csv'

# Omitting a lot of sanity checks to save time :)
if filename_convoy_data.endswith('.xlsx'):
    df = pd.read_excel(filename_convoy_data, sheet_name='Vehicles')
    csv_filename = get_filename_without_ext(filename_convoy_data) + '.csv'
    df.to_csv(csv_filename)
    print_excel_import_result(df)
elif filename_convoy_data.endswith('.csv'):
    df = pd.read_csv(filename_convoy_data)
else:
    print('Invalid input!')
    raise SystemExit(0)

# Clean cells and print to CSV
df = df.applymap(extract_int)
df.set_index('vehicle_id', inplace=True)
df.to_csv(filename_checked_csv)

# The result of the cleaner
cells_cell = 'cell' if checked == 1 else 'cells'
were_was = 'was' if checked == 1 else 'were'
print(f"{checked} {cells_cell} {were_was} corrected in {filename_checked_csv}")
