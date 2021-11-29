from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

class rocket_by_id(BaseModel):
    id: int

class citys_by_id(BaseModel):
    first_city: int
    second_city: int