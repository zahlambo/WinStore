from fastapi import FastAPI
from core.db import get_database
from model import *
from fastapi.middleware.cors import CORSMiddleware
from routers import app,user
app = FastAPI()
db = get_database()
collection = db["apps"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app.router)
app.include_router(user.router)