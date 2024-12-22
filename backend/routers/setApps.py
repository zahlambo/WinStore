from fastapi import APIRouter, HTTPException, Request,Depends
from utils.commonFunction import validateJwtFromCookies
from core.db import getDatabase



db = getDatabase()
router = APIRouter(
    prefix="/setApps",
    tags=["setApps"]
)

@router.put("/setAppsToUser")
async def addApps(apps: str, request: Request,token= Depends(validateJwtFromCookies)):
    token = token.get("Email")
  
    # Check if a user with the same Email already exists
    existing_user = await db["User"].find_one({"Email": token})

    if not existing_user:
        raise HTTPException(
            status_code=400, detail="User with the same Email does not exist")
    # Insert the apps for the user
    try:
        await db["user"].update_one({"Email": token}, {"$set": {"apps": apps}})
        return {"detail": "Apps updated successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Details: {e}")
    