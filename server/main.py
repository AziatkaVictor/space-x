from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

class login(BaseModel):
    username: str
    password: str

class User(BaseModel):
    login: str

class rocket_by_id(BaseModel):
    id: int

class citys_by_id(BaseModel):
    first_city: int
    second_city: int

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

@app.post("/is_admin/")
def is_user_exist(item: User):
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT is_admin FROM Users WHERE username == '" + item.login + "';"
        cursor.execute(sqlite_select_query)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

@app.post("/rocket_by_id/")
def rocket_by_id(item: rocket_by_id):
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM Rockets WHERE id = " + str(item.id) + ";"
        cursor.execute(sqlite_select_query)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

@app.post("/citys_by_id/")
def citys_by_id(item: citys_by_id):
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM Citys WHERE id = " + str(item.first_city) + " or " + str(item.second_city) + ";"
        cursor.execute(sqlite_select_query)
        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

@app.get("/rockets/")
def return_rockets():
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM Rockets;"
        cursor.execute(sqlite_select_query)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

@app.get("/cities/")
def return_cities():
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM Citys;"
        cursor.execute(sqlite_select_query)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False

@app.get("/flights/")
def return_flights():
    try:
        sqlite_connection = sqlite3.connect('spacex_database.db')
        cursor = sqlite_connection.cursor()

        sqlite_select_query = "SELECT * FROM Flights;"
        cursor.execute(sqlite_select_query)

        return cursor.fetchall()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
        return False