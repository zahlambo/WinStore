from fastapi import HTTPException, Request
from jose import jwt, JWTError
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


secretKey = os.getenv("SECRET_KEY")
algorithm = "HS256"

def validateJwtFromCookies(request: Request):
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload = jwt.decode(token, secretKey, algorithms=[algorithm])
        Email: str = payload.get("Email")
        if Email is None or datetime.now() > datetime.fromtimestamp(payload.get("exp", 0)):
            raise HTTPException(status_code=403, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload  