import json


def save_to_json(rows, json_filename, table_name):
    rows_to_export = [dict(ix) for ix in rows if ix['score'] > 3]
    for row in rows_to_export:
        del row['score']
    json_data = json.dumps(rows_to_export)
    formatted_json_str = f'{{"{table_name}" : {json_data}}}'
    with open(json_filename, "w") as file:
        file.write(formatted_json_str)
    return len(rows_to_export)
