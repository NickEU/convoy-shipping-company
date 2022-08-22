from dict2xml import dict2xml
from collections import OrderedDict


def save_to_xml(rows, save_to_filename, table_name, entity_name):
    rows_to_export = [dict(ix) for ix in rows if ix['score'] <= 3]
    for row in rows_to_export:
        del row['score']
    xml_elements = [f"<{entity_name}>\n{dict2xml(OrderedDict(row))}\n</{entity_name}>\n"
                    for row in rows_to_export]
    final_xml = f"<{table_name}>\n{''.join(xml_elements)}</{table_name}>"

    with open(save_to_filename, "w") as file:
        file.write(final_xml)
    return len(rows_to_export)
