import requests
import json

API = 'http://127.0.0.1:8000'

def user_auth(login, password):
    data = {
        "username": login,
        "password": password
    }

    r = requests.post(API + '/login/', data=json.dumps(data))
    return (r.text)

def is_admin(login):
    data = {
        "login": login
    }

    r = requests.post(API + '/is_admin/', data=json.dumps(data))

    if r.json()[0][0].lower() == 'true':
        return True
    else:
        return False

def rockets():
    r = requests.get(API + '/rockets/')
    return (r.json())

def flights():
    r = requests.get(API + '/flights/')
    return (r.json())

def rocket_by_id(id):
    data = {
        "id": id
    }

    r = requests.post(API + '/rocket_by_id/', data=json.dumps(data))
    return (r.json())

def citys_by_id(first, second):
    data = {
        "first_city": first,
        "second_city": second
    }

    r = requests.post(API + '/citys_by_id/', data=json.dumps(data))
    return (r.json())