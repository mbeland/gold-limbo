#!/usr/bin/env python
# Create SQLite db, prep for plugin use
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a SQLite db connection """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a db table """
    try:
        c = conn.curcsor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    db_location = "goldstars.sqlite"
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                id integer PRIMARY KEY,
                                name text NOT NULL,
                                main integer,
                                secondary integer,
                                drawer text
                            );"""
    sql_create_prizes_table = """ CREATE TABLE IF NOT EXISTS prizes (
                                id integer PRIMARY KEY,
                                main text NOT NULL,
                                secondary text NOT NULL
                            );"""

    conn = create_connection(db_location)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_prizes_table)
    else:
        print("Error: Cannot create database connection.\n")
    conn.close()


if __name__ == '__main__':
    main()
