from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from core.db import get_database
from fastapi.responses import JSONResponse
from fastapi import Request

db = get_database()
collection = db["User"]
# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    user = await collection.find_one({"Email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email")

    if not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    token_data = {"sub": user["Email"], "username": user["username"]}
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Set the token in an HTTP-only cookie
    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Prevent JavaScript access
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Set expiration
    )
    return response

@router.post("/logout")
async def logout():
    response = JSONResponse({"message": "Logout successful"})
    response.delete_cookie("access_token")
    return response




def validate_jwt_from_cookies(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None or datetime.now() > datetime.fromtimestamp(payload.get("exp", 0)):
            raise HTTPException(status_code=403, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload  # Return the payload if needed (e.g., for user info)

# Protected route
@router.get("/protected")
async def protected_route(payload: dict = Depends(validate_jwt_from_cookies)):
    return {"message": f"Welcome, {payload['sub']}!"}
