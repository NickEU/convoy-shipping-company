def announce_cleaning_result(cleaned, filename):
    print(f"{cleaned} cell{s_if_plural(cleaned)} {was_were(cleaned)} corrected in {filename}")


def announce_db_insert_result(count, db_name):
    print(f'{count} record{s_if_plural(count)} '
          f'{was_were(count)} inserted into {db_name}')


def announce_json_save_result(count, json_filename):
    print(f'{count} vehicle{s_if_plural(count)} {was_were(count)} saved into {json_filename}')


def was_were(num):
    return 'was' if num == 1 else 'were'


def s_if_plural(num):
    return '' if num == 1 else 's'
