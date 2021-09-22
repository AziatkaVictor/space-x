from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class login(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/login/")
def is_user_exist(item: login):
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT username, password FROM Users;"
        cursor.execute(sqlite_select_query)
        for i in cursor.fetchall():
            if i[0] == item.username and i[1] == item.password:
                return True

        return False

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False