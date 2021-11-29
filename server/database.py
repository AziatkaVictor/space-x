import sqlite3


def run_query(text):
    try:
        sqlite_connection = sqlite3.connect('data/spacex_database.db')
        cursor = sqlite_connection.cursor()
        cursor.execute(text)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False