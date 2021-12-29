#!/usr/bin/env python3
import sqlite3


def connect_sqlite(DB):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    return conn, cursor


def get_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()


def get_row(cursor, table):
    cursor.execute(f"SELECT * FROM {table};")
    return cursor.fetchone()


def get_rows(cursor, table):
    cursor.execute(f"SELECT * FROM {table};")
    return cursor.fetchall()


def get_column_names(row):
    return row.keys()


def get_table_info(cursor, table):
    cursor.execute(f'pragma table_info({table})')
    return cursor.fetchall()


def get_table_row(cursor, table):
    cursor.execute(f'pragma table_info({table})')
    return cursor.fetchall()


def view_table_info(cursor, table):
    info = get_table_info(cursor, table)
    print(f"\n\n## {table}\n")
    print('|{:^10s}|{:^21s}|{:^18s}|{:^11s}|{:^14s}|{:^13s}|'.format(
        "-"*10,
        "-"*21,
        "-"*18,
        "-"*11,
        "-"*14,
        "-"*13,
        )    
    )
    print('|{:^10s}|{:^21s}|{:^18s}|{:^11s}|{:^14s}|{:^13s}|'.format(
        "ID",
        "Name",
        "Type",
        "NotNull",
        "DefaultVal",
        "PrimaryKey"
        )
    )
    print('|{:^10s}|{:^21s}|{:^18s}|{:^11s}|{:^14s}|{:^13s}|'.format(
        "-"*10,
        "-"*21,
        "-"*18,
        "-"*11,
        "-"*14,
        "-"*13,
        )    
    )

    for i in info:
        print('|{:^10s}|{:^21s}|{:^18s}|{:^11s}|{:^14s}|{:^13s}|'.format(
            f'{i[0]}',
            f'{i[1]}',
            f'{i[2]}',
            f'{i[3]}',
            f'{i[4]}',
            f'{i[5]}'
        )
    )

