from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int
