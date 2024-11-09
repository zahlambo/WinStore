from fastapi import FastAPI, HTTPException,Depends
from db import get_database
import json
from model import *
from typing import List
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
    # Check if an item with the same name or ID already exists
    existing_item = await collection.find_one({"$or": [{"name": item.name}, {"id": item.id}]})
    
    if existing_item:
        raise HTTPException(status_code=400, detail="Item with the same name or ID already exists")

    await collection.insert_one({"name": item.name, "icon": item.icon, "id": item.id})
    return "Item added successfully!"


@app.get("/getAllItems")
async def getAllItems(name: Optional[str] = None,id: Optional[str] = None):
    query = {}

    if name:
        query["name"] = re.compile(name, re.IGNORECASE)
    elif id:
        query["id"] = re.compile(id, re.IGNORECASE)

    items = await collection.find(query, {"_id": 0,"icon":0}).to_list()
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
