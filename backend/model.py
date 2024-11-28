from pydantic import BaseModel,Field,EmailStr
from typing import Optional,Union

class AddItem(BaseModel):
    name: str
    icon: str
    id: str
class searchItems(AddItem):
    name: Optional[str] = None
    id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str = Field(..., title="Username", description="Username of the user", example="potato",min_length=4,max_length=20)
    Email: EmailStr = Field(..., title="Email", description="Email of the user", example="example@gmail.com")
    password: str = Field(..., title="Password", description="Password of the user", example="password",min_length=6,max_length=20)
    first_name: str = Field(..., title="First Name", description="First Name of the user", example="John",min_length=4,max_length=20)
    last_name: str = Field(..., title="Last Name", description="Last Name of the user", example="Doe")
    apps: str = Field(default='winget install', title="Apps", description="Apps of the user", example="app1 app2")
    role: str = Field(default='User', title="Role of the user", description="Role of the user", example="admin")

class updateUser(BaseModel):
    username: str =Field(..., title="Username", description="Username of the user", example="potato",min_length=4,max_length=20)
    password: str =Field(..., title="Password", description="Password of the user", example="password",min_length=6,max_length=20)
    first_name: str = Field(..., title="First Name", description="First Name of the user", example="John",min_length=4,max_length=20)
    last_name: str = Field(..., title="Last Name", description="Last Name of the user", example="Doe")
    role: str = Field(default='User', title="Role", description="Role of the user", example="admin")

class LoginRequest(BaseModel):
    identifier: Union[EmailStr,str]= Field(..., title="Email or username", description="Email/username of the user", example="example@gmail.com")
    password: str = Field(..., title="Password", description="Password of the user", example="password")
class getAllUser(BaseModel):
    username: str
    Email: EmailStr
    first_name: str
    last_name: str
    role: str