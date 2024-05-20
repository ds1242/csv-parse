import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from read_file import read_csv

def create_db(filename):
    # create db connection to sqlite db
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()



def main():
    file_path = '/./example_batch_records.csv'
    read_csv(file_path)


main()

if __name__ == '__main__':
    create_db("csv_db.db")