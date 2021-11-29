from fastapi import FastAPI
from models import *
import database
import sqlite3


app = FastAPI()

@app.get("/login/{username}-{password}")
def is_user_exist(username: str, password: str):
    if database.run_query(f"SELECT username, password FROM Users WHERE username == '{username}' and password == '{password}';"):
        return True
    else:
        return False
        
@app.get("/is_admin/{username}")
def is_user_admin(username: str):
    return database.run_query(f"SELECT is_admin FROM Users WHERE username == '{username}';")

@app.get("/rocket_by_id/{rocket_id}")
def rocket_by_id(rocket_id: int):
    return database.run_query(f"SELECT * FROM Rockets WHERE id = {rocket_id};")

@app.get("/citys_by_id/{city_id}")
def citys_by_id(city_id: int):
    return database.run_query(f"SELECT * FROM Citys WHERE id = {city_id};")

@app.get("/rockets/")
def return_rockets():
    return database.run_query("SELECT * FROM Rockets;")

@app.get("/cities/")
def return_cities():
    return database.run_query("SELECT * FROM Citys;")

@app.get("/flights/")
def return_flights():
    return database.run_query("SELECT * FROM Flights;")