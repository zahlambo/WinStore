from fastapi import APIRouter, Depends, HTTPException
from model import *
from core.db import get_database
import re
import bcrypt

router = APIRouter()
db = get_database()
collection = db["User"]

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@router.post("/addUser", response_model=str)
async def addUser(user: User = Depends(User)):
    # Check if a user with the same username already exists
    existing_user = await collection.find_one({"username": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with the same username already exists")

    # Hash the password before saving
    hashed_password = hash_password(user.password)
    await collection.insert_one({"username": user.username,"Email":user.email, "password": hashed_password,"first_name":user.first_name,"last_name":user.last_name})
    return "User added successfully!"