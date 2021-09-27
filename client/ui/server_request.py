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

def rockets():
  r = requests.get(API + '/rockets/')
  return (r.json())