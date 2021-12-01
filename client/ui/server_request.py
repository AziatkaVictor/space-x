import requests

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