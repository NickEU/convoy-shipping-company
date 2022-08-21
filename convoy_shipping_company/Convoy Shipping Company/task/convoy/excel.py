import pandas as pd
from misc import was_were, s_if_plural


def process_excel_input(excel_filename, save_to):
    df = pd.read_excel(excel_filename, sheet_name='Vehicles')
    df.to_csv(save_to, index=False)
    print_excel_import_result(df, save_to)


def print_excel_import_result(df_input, csv_filename):
    row_cnt = df_input.shape[0]
    print(f"{row_cnt} line{s_if_plural(row_cnt)}"
          f" {was_were(row_cnt)} imported to {csv_filename}")
