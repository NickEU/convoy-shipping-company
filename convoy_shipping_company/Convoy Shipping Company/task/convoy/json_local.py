from db import get_rows_from_table


def save_to_json(db_filename, table_name, json_filename):
    result = get_rows_from_table(db_filename, table_name)
    formatted_json_str = f'{{"{table_name}" : {result.json_result}}}'
    with open(json_filename, "w") as file:
        file.write(formatted_json_str)
    return result.rows_returned
