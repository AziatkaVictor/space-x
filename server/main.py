from fastapi import FastAPI
from models import *
import database
import uvicorn


app = FastAPI()

@app.get("/login/{username}-{password}")
def is_user_exist(username: str, password: str):
    if database.run_query(f"SELECT username, password FROM Users WHERE username == '{username}' and password == '{password}';", True):
        return True
    else:
        return False
        
@app.get("/is_admin/{username}")
def is_user_admin(username: str):
    return database.run_query(f"SELECT is_admin FROM Users WHERE username == '{username}';", True)

@app.get("/rocket_by_id/{rocket_id}")
def rocket_by_id(rocket_id: int):
    return database.run_query(f"SELECT * FROM Rockets WHERE id = {rocket_id};", True)

@app.get("/citys_by_id/{city_id}")
def citys_by_id(city_id: int):
    return database.run_query(f"SELECT * FROM Citys WHERE id = {city_id};", True)

@app.get("/citys_without_this/{city_name}")
def citys_without_this(city_name: str):
    return database.run_query(f"SELECT * FROM Citys WHERE name <> '{city_name}';", False)

@app.get("/rockets/")
def return_rockets():
    return database.run_query("SELECT * FROM Rockets;", False)

@app.get("/cities/")
def return_cities():
    return database.run_query("SELECT * FROM Citys;", False)

@app.get("/flights/")
def return_flights():
    return database.run_query("SELECT * FROM Flights;", False)

@app.get("/articles/")
def return_articles():
    return database.run_query("SELECT * FROM Articles;", False)

@app.get("/get_id_by_name/{table}-{name}")
def get_id_by_name(table : str, name : str):
    return database.run_query(f"SELECT id FROM {table} WHERE name = '{name}';", True)

@app.post("/add_flight/")
def add_flight(item : Rocket):
    if database.post_data(f"INSERT INTO Flights ('name', 'rocket', 'cost', 'date_and_time', 'first_city', 'second_city') VALUES ('{item.name}', {item.rocket}, {item.cost}, '{item.date}', {item.first_city}, {item.second_city});"):
        return 'OK'
    else:
        return item

@app.post("/edit_flight/")
def add_flight(item : EditRocket):
    if database.post_data(f"UPDATE Flights SET 'name' = '{item.name}', 'rocket' = {item.rocket}, 'cost' = {item.cost}, 'date_and_time' = '{item.date}', 'first_city' = {item.first_city}, 'second_city' = {item.second_city} WHERE id = {item.id};"):
        return 'OK'
    else:
        return item

@app.post("/delete_flight/{id}")
def delete_flight(id : int):
    database.delete_data(f'DELETE FROM Flights WHERE id = {id};')
    return 'OK'

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)