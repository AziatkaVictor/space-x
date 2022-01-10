import requests
from requests.api import request


API = 'http://127.0.0.1:8000'

def user_auth(username, password):
    return requests.get(f'{API}/login/{username}-{password}').json()

def is_admin(username):
    return requests.get(f'{API}/is_admin/{username}').json()['is_admin']

def rockets():
    return requests.get(f'{API}/rockets/').json()

def flights():
    return requests.get(f'{API}/flights/').json()

def articles():
    return requests.get(f'{API}/articles/').json()

def citys():
    return requests.get(f'{API}/cities/').json()

def rockets_logos():
    return requests.get(f'{API}/rockets_logos/').json()

def rocket_by_id(id):
    return requests.get(f'{API}/rocket_by_id/{id}').json()

def citys_by_id(id):
    return requests.get(f'{API}/citys_by_id/{id}').json()

def flight_by_id(id):
    return requests.get(f'{API}/flight_by_id/{id}').json()

def status_by_id(id):
    return requests.get(f'{API}/status_by_id/{id}').json()
    
def get_count_of_atrticles(id):
    return requests.get(f'{API}/get_count_of_atrticles/{id}').json()['count']

def citys_without_this(name):
    return requests.get(f'{API}/citys_without_this/{name}').json()

def get_id_by_name(table, name):
    return requests.get(f'{API}/get_id_by_name/{table}-{name}').json()['id']

def get_status_id_by_type(type):
    return requests.get(f'{API}/get_status_id_by_type/{type}').json()['id']

def add_flight(name, rocket, cost, date, first_city, second_city):
    data = {
        "name" : f"{name}", 
        "rocket" : rocket, 
        "cost" : cost,
        "date" : f"{date}", 
        "first_city" : first_city, 
        "second_city" : second_city
    }
    print(requests.post(f'{API}/add_flight/', json=data).json())

def edit_flight(id, name, rocket, cost, date, first_city, second_city):
    data = {
        "id" : id,
        "name" : f"{name}", 
        "rocket" : rocket, 
        "cost" : cost,
        "date" : f"{date}", 
        "first_city" : first_city, 
        "second_city" : second_city
    }
    print(requests.post(f'{API}/edit_flight/', json=data).json())

def change_status_article(id, status_id):
    print(requests.post(f'{API}/change_status_article/{id}-{status_id}').json())

def delete_flight(id):
    return requests.post(f'{API}/delete_flight/{id}').text