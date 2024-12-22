from fastapi import FastAPI
from core.db import getDatabase
from model import *
from fastapi.middleware.cors import CORSMiddleware
from routers import apps,user,auth,setApps
app = FastAPI()
db = getDatabase()
collection = db["apps"]

@app.on_event("startup")
async def startup_event():
    await db["user"].create_index("username", unique=True)
    await db["user"].create_index("email", unique=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apps.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(setApps.router)

