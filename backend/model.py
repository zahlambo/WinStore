from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class AddItem(BaseModel):
    name: str
    icon: str
    id: str
class searchItems(AddItem):
    name: Optional[str] = None
    id: Optional[str] = None

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: EmailStr
    password: str     
    first_name: str
    last_name: str
