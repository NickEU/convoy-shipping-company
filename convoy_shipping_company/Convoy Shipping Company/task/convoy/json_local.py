import json


def save_to_json(rows, json_filename, table_name):
    json_data = json.dumps([dict(ix) for ix in rows])
    formatted_json_str = f'{{"{table_name}" : {json_data}}}'
    with open(json_filename, "w") as file:
        file.write(formatted_json_str)
    return len(rows)
