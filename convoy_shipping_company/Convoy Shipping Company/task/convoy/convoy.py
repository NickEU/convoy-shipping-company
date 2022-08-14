# Prompt the user to give a name for the input Excel file
# (complete with the .xlsx extension). For the prompt message, use Input file name followed by a newline.
# Import a sheet named Vehicles from the entered XLSX file to a CSV file.
# The CSV file should have the same name as the XLSX file,
# but it should have the .csv extension (you can take the test table below).
# Your program should import only the headers, omitting indexes.
# Count the number of entries imported to the CSV file
# and print them out to standard output; the headers should not be counted.
# Your program should output the following message: X lines were imported to %file_name%.csv
# or 1 line was imported to %file_name%.csv , where X is the number of imported lines.
# For example: 4 lines were imported to convoy.csv


import pandas as pd

filename_convoy_data = input('Input file name\n')

# omitting a lot of sanity checks to save time :)
filename_without_ext = filename_convoy_data.split('.xlsx')[0]
csv_filename = filename_without_ext + '.csv'
df = pd.read_excel(filename_convoy_data, sheet_name='Vehicles', index_col='vehicle_id')
df.to_csv(csv_filename)
rows_imported = df.shape[0]
lines_line = '' if rows_imported == 1 else 's'
were_was = 'was' if rows_imported == 1 else 'were'
print(f"{rows_imported} line{lines_line} {were_was} imported to {csv_filename}")
