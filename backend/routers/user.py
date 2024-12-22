from fastapi import APIRouter, Depends, HTTPException
from model import *
from core.db import getDatabase
import re
import bcrypt
from utils.commonFunction import validateJwtFromCookies
from pymongo.errors import DuplicateKeyError
from typing import List

router = APIRouter(prefix="/apps/user", tags=["User"])
db = getDatabase()
collection = db["User"]


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


@router.get("/User")
async def getAllUserFromDB():
    pipeline = [{"$project": {"_id": 0}}]

    users = await collection.aggregate(pipeline).to_list()
    return users


@router.post("/User", response_model=str)
async def addUser(user: User = Depends(User)):
    # Hash the password before saving
    hashed_password = hash_password(user.password)
    try:
        await collection.insert_one(
            {
                "username": user.username,
                "Email": user.Email,
                "password": hashed_password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "apps": user.apps,
                "role": user.role,
            }
        )
    except DuplicateKeyError as e:
        if "Email" in str(e):
            raise HTTPException(status_code=400, detail="Email is already registered")
        elif "username" in str(e):
            raise HTTPException(status_code=400, detail="Username is already taken")
        else:
            raise HTTPException(
                status_code=400, detail="A duplicate key error occurred"
            )
    return {"detail":"User added successfully!"}


@router.put("/User", response_model=str)
async def updateUser(
    user: updateUser = Depends(updateUser), token=Depends(validateJwtFromCookies)
):
    try:
        token = token.get("Email")
    except HTTPException as e:
        return {"detail": f"Authentication failed: {e}"}
    # Check if a user with the same username already exists

    existing_user = await collection.find_one({"Email": token})
    # Hash the password before saving
    if not existing_user:
        raise HTTPException(
            status_code=400, detail="User with the same username does not exist"
        )
    hashed_password = hash_password(user.password)
    await collection.update_one(
        {"Email": token},
        {
            "$set": {
                "username": user.username,
                "password": hashed_password,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "apps": user.apps,
                "role": user.role,
            }
        },
    )
    return {"detail": "User updated successfully"}


@router.delete("/User", response_model=str)
async def deleteUser(token=Depends(validateJwtFromCookies)):
    try:
        token = token.get("Email")
    except HTTPException as e:
        return (e.status_code, {"detail": "Authentication failed: Invalid token"})

    existing_user = await collection.find_one({"Email": token})
    if existing_user:
        await collection.delete_one({"Email": token})
    else:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted successfully!"}
