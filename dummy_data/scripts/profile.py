import pymysql
import csv

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'gd456nds',
    'database': 'travel',
    'charset': 'utf8mb4'
}

csv_file_path = r'dummy_data\csv\profile.csv'

table_name = 'customer_profile'

try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO {
            table_name} ({', '.join(headers)}) VALUES ({placeholders})"

        for row in csv_reader:
            cursor.execute(insert_query, row)

    connection.commit()
    print("Data inserted successfully!")

except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
