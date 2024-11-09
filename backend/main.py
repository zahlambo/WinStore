from fastapi import FastAPI
from db import get_database
import json
from model import *
import re
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
db = get_database()
collection = db["apps"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)


@app.post("/addItem", response_model=str)
async def addItem(item: AddItem):
    await collection.insert_one({"name": item.name, "icon": item.icon, "id": item.id})
    return "Item added successfully!"


@app.get("/getAllItems")
async def getAllItems():
    items = await collection.find({}, {"_id": 0}).to_list()
    return items


@app.get("/items/{appQuery}", response_model=str)
async def readItem(appQuery: str):
    wingetScript = "winget install "
    for itemName in appQuery.split(","):
        # Removing spaces from the string
        itemName = itemName.strip().replace(" ", "")
        item = await collection.find_one({"name": re.compile(itemName, re.IGNORECASE)})
        if item:
            wingetScript += item['id'] + " "
    return wingetScript
