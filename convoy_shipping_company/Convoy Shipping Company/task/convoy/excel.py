import pandas as pd


def process_excel_input(excel_filename, save_to):
    df = pd.read_excel(excel_filename, sheet_name='Vehicles')
    df.to_csv(save_to, index=False)
    print_excel_import_result(df, save_to)


def print_excel_import_result(df_input, csv_filename):
    rows_imported = df_input.shape[0]
    lines_line = '' if rows_imported == 1 else 's'
    was_were = 'was' if rows_imported == 1 else 'were'
    print(f"{rows_imported} line{lines_line} {was_were} imported to {csv_filename}")
