from pydantic import BaseModel
from datetime import datetime


class Rocket(BaseModel):
    name : str
    rocket : int
    cost : int
    date : datetime
    first_city : int
    second_city : int