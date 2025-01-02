import pymysql
import sqlite3
import psycopg2
import csv

# Configuration for databases
db_type = "sqlite"  # Change this to "sqlite", "postgresql", or "mysql"

# MySQL configuration
mysql_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'gd456nds',
    'database': 'user',
    'charset': 'utf8mb4'
}

# SQLite configuration
sqlite_db_path = "db.sqlite3"

# PostgreSQL configuration
postgres_config = {
    'host': '127.0.0.1',
    'user': 'postgres',
    'password': 'your_password',
    'database': 'user',
    'port': 5432
}

csv_file_path = r'dummy_data/csv/hotel_rooms.csv'
table_name = 'accommodation_hotelroom'


def connect_to_db():
    if db_type == "mysql":
        return pymysql.connect(**mysql_config)
    elif db_type == "sqlite":
        return sqlite3.connect(sqlite_db_path)
    elif db_type == "postgresql":
        return psycopg2.connect(**postgres_config)
    else:
        raise ValueError("Unsupported database type")


def insert_data():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Open CSV file
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)

            if db_type == "mysql" or db_type == "postgresql":
                placeholders = ', '.join(['%s'] * len(headers))
            elif db_type == "sqlite":
                placeholders = ', '.join(['?'] * len(headers))

            insert_query = f"INSERT INTO {
                table_name} ({', '.join(headers)}) VALUES ({placeholders})"

            for row in csv_reader:
                cursor.execute(insert_query, row)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except (pymysql.MySQLError, sqlite3.Error, psycopg2.Error) as e:
        print(f"Error: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    insert_data()
