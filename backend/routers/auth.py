from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from core.db import getDatabase
from fastapi.responses import JSONResponse
from fastapi import Request
from model import LoginRequest
from utils.commonFunction import validateJwtFromCookies


db = getDatabase()
userCollection = db["User"]
# Load environment variables
load_dotenv()

secretKey = os.getenv("SECRET_KEY")
algorithm = "HS256"
accessTokenExpireMinutes = os.getenv("ExpireMinutes")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
async def login(request: LoginRequest):
    # Find user by email or username
    user = await userCollection.find_one(
        {"$or": [{"Email": request.identifier}, {"username": request.identifier}]}
    )
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or username")

    # Verify password
    if not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    # Generate token
    tokenData = {"Email": user["Email"], "username": user["username"]}
    expire = datetime.now() + timedelta(minutes=accessTokenExpireMinutes)
    tokenData.update({"exp": expire})
    token = jwt.encode(tokenData, secretKey, algorithm=algorithm)

    # Set the token in an HTTP-only cookie
    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(
        key="accessToken",
        value=token,
        httponly=True,  # Prevent JavaScript access
        max_age=accessTokenExpireMinutes * 60,  # Set expiration
    )
    return response

@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie("accessToken")
    return response



@router.get("/getCurrentUser")
async def getCurrentUser(payload: dict = Depends(validateJwtFromCookies)):
    return payload