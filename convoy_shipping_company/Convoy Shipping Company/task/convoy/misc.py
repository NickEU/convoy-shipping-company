def announce_cleaning_result(cleaned, filename):
    print(f"{cleaned} cell{s_if_plural(cleaned)} {was_were(cleaned)} corrected in {filename}")


def announce_db_insert_result(rows_inserted, db_name):
    print(f'{rows_inserted} record{s_if_plural(rows_inserted)} '
          f'{was_were(rows_inserted)} inserted into {db_name}')


def was_were(num):
    return 'was' if num == 1 else 'were'


def s_if_plural(num):
    return '' if num == 1 else 's'
