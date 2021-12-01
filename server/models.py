from pydantic import BaseModel
import datetime


class Post_rocket(BaseModel):
    name : str
    rocket : int
    cost : int
    date : datetime.datetime
    first_city : int
    second_city : int