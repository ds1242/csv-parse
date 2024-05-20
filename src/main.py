import csv
import sqlite3



def connect_to_database(db_path):
    if db_path:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        return connection, cursor
    else:
        print('No DB Path Provided')

def create_table(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS batch_jobs (
    ID int,
    SUBMITTED_AT varchar(50)
    NODES_USED int
    )
    """
    cursor.execute(create_table)


def read_csv(path, cursor):
    with open(path) as csvfile:
        file_reader = csv.reader(csvfile, newline='')
        next(file_reader)
        for row in file_reader:
            insert_sql = 'INSERT INTO batch_jobs (ID, SUBMITTED_AT, NODES_USED) VALUES (?, ?, ?)'
            cursor.execute(insert_sql, row)
    print('Done adding rows')

def commit_and_close(connection):
    connection.commit()
    connection.close()


def main():
    db_path = './src/batch_jobs.db'
    csv_path = './example_batch_records.csv'
    connection, cursor = connect_to_database(db_path)

    create_table(cursor)

    read_csv(csv_path, cursor)

    commit_and_close(connection)


main()