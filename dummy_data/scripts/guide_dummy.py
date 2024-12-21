import pymysql
import csv
from django.conf import settings
from django.contrib.auth.hashers import make_password

settings.configure(
    PASSWORD_HASHERS=[
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.Argon2PasswordHasher',
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]
)


db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'gd456nds',
    'database': 'travel',
    'charset': 'utf8mb4'
}

csv_file_path = r'dummy_data/csv/Guides.csv'

table_name = 'guide_guide'

try:
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)

        password_column_index = headers.index("password")

        placeholders = ', '.join(['%s'] * len(headers))
        insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"

        for row in csv_reader:
            processed_row = row[:]  
            password = row[password_column_index]

            hashed_password = make_password(password)
            processed_row[password_column_index] = hashed_password

            cursor.execute(insert_query, processed_row)

    connection.commit()
    print("Data inserted successfully!")

except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()


