import requests
from requests.api import request


API = 'http://127.0.0.1:8000'

def user_auth(username, password):
    return requests.get(f'{API}/login/{username}-{password}').text

def is_admin(username):
    return requests.get(f'{API}/is_admin/{username}').json()['is_admin']

def rockets():
    return requests.get(f'{API}/rockets/').json()

def flights():
    return requests.get(f'{API}/flights/').json()

def citys():
    return requests.get(f'{API}/cities/').json()

def rocket_by_id(id):
    return requests.get(f'{API}/rocket_by_id/{id}').json()

def citys_by_id(id):
    return requests.get(f'{API}/citys_by_id/{id}').json()

def citys_without_this(name):
    return requests.get(f'{API}/citys_without_this/{name}').json()

def get_id_by_name(table, name):
    return requests.get(f'{API}/get_id_by_name/{table}-{name}').json()['id']

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

def delete_flight(id):
    return requests.post(f'{API}/delete_flight/{id}').text