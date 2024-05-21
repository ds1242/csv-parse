import csv
import sqlite3

def get_path_to_file():
    path_to_file = input('Please enter a path to the CSV file:\n')
    return path_to_file

def connect_to_database(db_path):
    if db_path:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        return connection, cursor
    else:
        print('No DB Path Provided')


def drop_table_if_exists(cursor):
    drop_table_sql = "DROP TABLE IF EXISTS batch_jobs"
    cursor.execute(drop_table_sql)


def create_table(cursor):
    create_table = """
    CREATE TABLE IF NOT EXISTS batch_jobs (
    ID int,
    SUBMITTED_AT varchar(50),
    NODES_USED int
    )
    """
    cursor.execute(create_table)


def read_csv(path, cursor):
    with open(path) as csvfile:
        file_reader = csv.reader(csvfile, delimiter=",")
        next(file_reader)
        for row in file_reader:
            insert_sql = 'INSERT INTO batch_jobs (ID, SUBMITTED_AT, NODES_USED) VALUES (?, ?, ?)'
            batch_clean = ''.join(i for i in row[0] if i.isdigit())
            
            batch_number = int(batch_clean)
            submitted_at= row[1]
            nodes_used = row[2]
            
            cursor.execute(insert_sql, (batch_number, submitted_at, nodes_used))
    print('Done adding rows')


def commit_and_close(connection):
    connection.commit()
    connection.close()


def main():
    db_path = './src/batch_jobs.db'
    csv_path = get_path_to_file()
    connection, cursor = connect_to_database(db_path)

    drop_table_if_exists(cursor)

    create_table(cursor)

    read_csv(csv_path, cursor)

    commit_and_close(connection)


main()