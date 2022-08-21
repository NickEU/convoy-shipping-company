import sqlite3
import json


class DatabaseSaveResult:

    def __init__(self, records_inserted):
        self.records_inserted = records_inserted


def save_to_sqlite(db_filename, table_name, data_ready_for_db):
    conn = sqlite3.connect(db_filename)
    cursor_name = conn.cursor()
    columns = data_ready_for_db.columns
    sql_list_of_columns = ",".join([f"{x} INT NOT NULL" for x in columns])

    sql_drop_table_if_exists = f"DROP TABLE IF EXISTS {table_name}"
    cursor_name.execute(sql_drop_table_if_exists)

    sql_query_create_table = f"""CREATE TABLE {table_name}({sql_list_of_columns},
        PRIMARY KEY ({columns[0]})
    );"""

    cursor_name.execute(sql_query_create_table)
    records_inserted = 0
    for idx, row in data_ready_for_db.iterrows():
        column_names = ",".join([x for x in row.index])
        values = ",".join([str(x) for x in row.values])
        # you cannot appreciate the beauty of SQLAlchemy and df.to_sql() without experiencing this pain
        sql_query_insert_row = f"""INSERT INTO {table_name} ({column_names}) VALUES ({values});"""
        result = cursor_name.execute(sql_query_insert_row)
        records_inserted += result.rowcount

    conn.commit()
    conn.close()

    return DatabaseSaveResult(records_inserted)


class SelectQueryResult:
    def __init__(self, rows_returned, json_result):
        self.rows_returned = rows_returned
        self.json_result = json_result


def get_rows_from_table(db_filename, table_name):
    conn = sqlite3.connect(db_filename)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    db = conn.cursor()

    rows = db.execute(f'''
    SELECT * from {table_name}
    ''').fetchall()

    conn.commit()
    conn.close()

    return SelectQueryResult(len(rows), json.dumps([dict(ix) for ix in rows]))
