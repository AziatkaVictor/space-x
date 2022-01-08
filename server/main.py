from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import *
import database
import uvicorn


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates/")

@app.get("/")
def form_post(request: Request):
    flights = database.run_query("SELECT Flights.*, Rockets.max_people_count, (SELECT count(*) FROM Articles WHERE Articles.flight = Flights.id) as count, (SELECT name FROM Citys WHERE Citys.id = Flights.first_city) as start, (SELECT name FROM Citys WHERE Citys.id = Flights.second_city) as end FROM Flights JOIN Rockets ON Rockets.id = Flights.rocket WHERE count <> Rockets.max_people_count;", False)
    return templates.TemplateResponse('index.html', context={'request': request, 'flights' : flights})

@app.post("/")
def form_post(request: Request, name: str = Form(...), docs: str = Form(...), select: str = Form(...)):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = database.run_query(f"SELECT id FROM Statuses WHERE type = 'waited';", True)['id']
    if database.post_data(f"INSERT INTO Articles ('name', 'date', 'docs', 'status', 'flight') VALUES ('{name}', '{date}', '{docs}', {status}, {select});") is not None:
        return templates.TemplateResponse('done.html', context={'request': request})
    else:
        return templates.TemplateResponse('error.html', context={'request': request})

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

@app.get("/flight_by_id/{flight_id}")
def flight_by_id(flight_id: int):
    return database.run_query(f"SELECT * FROM Flights WHERE id = {flight_id};", True)

@app.get("/status_by_id/{status_id}")
def status_by_id(status_id: int):
    return database.run_query(f"SELECT * FROM Statuses WHERE id = {status_id};", True)

@app.get("/citys_without_this/{city_name}")
def citys_without_this(city_name: str):
    return database.run_query(f"SELECT * FROM Citys WHERE name <> '{city_name}';", False)

@app.get("/get_count_of_atrticles/{flight_id}")
def get_count_of_atrticles(flight_id: int):
    return database.run_query(f"SELECT COUNT(*) as count FROM Articles WHERE flight = {flight_id} and status = 2;", True)

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

@app.get("/rockets_logos/")
def rockets_logos():
    return database.run_query("SELECT DISTINCT img as url FROM Rockets;", False)

@app.get("/get_id_by_name/{table}-{name}")
def get_id_by_name(table : str, name : str):
    return database.run_query(f"SELECT id FROM {table} WHERE name = '{name}';", True)
    
@app.get("/get_status_id_by_type/{type}")
def get_status_id_by_type(type : str):
    return database.run_query(f"SELECT id FROM Statuses WHERE type = '{type}';", True)

@app.post("/add_flight/")
def add_flight(item : Rocket):
    if database.post_data(f"INSERT INTO Flights ('name', 'rocket', 'cost', 'date_and_time', 'first_city', 'second_city') VALUES ('{item.name}', {item.rocket}, {item.cost}, '{item.date}', {item.first_city}, {item.second_city});"):
        return 'OK'
    else:
        return item

@app.post("/change_status_article/{id}-{status_id}")
def change_status_article(id : int, status_id : int):
    if database.post_data(f"UPDATE Articles SET 'status' = {status_id} WHERE id = {id};"):
        return 'OK'
    else:
        return 'ERROR'
 
@app.post("/edit_flight/")
def edit_flight(item : EditRocket):
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