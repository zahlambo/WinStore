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


@app.put("/updateItem", response_model=str)
def updateItem(name: Optional[str] = None,id: Optional[str] = None, item: AddItem = Depends(AddItem)):
    query = {}
    if name:
        query["name"] = name
    elif id:
        query["id"] = id
    else:
        raise HTTPException(status_code=400, detail="Name or ID must be provided")

    items = collection.update_one(query)
    return items


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
    if name and id:
        query["$or"] = [{"name": re.compile(name, re.IGNORECASE)}, {"id": re.compile(id, re.IGNORECASE)}]
    elif id:
        query["id"] = re.compile(id, re.IGNORECASE)

    elif name:
        query["name"] = re.compile(name, re.IGNORECASE)
    

    items = await collection.find(query, {"_id": 0,}).to_list()
    return items


@app.get("/items/{appQuery}", response_model=str)
async def readItem(appQuery: str):
    wingetScript = "winget install "
    itemNames=[ name.strip().replace(" ", "") for name in appQuery.split(",")]
    items= await collection.find({"name": {"$in": [re.compile(name, re.IGNORECASE) for name in itemNames]}}).to_list()

    if items:
        wingetScript += " ".join([item["id"] for item in items])
    else:
        raise HTTPException(status_code=404, detail="Items not found")
    return wingetScript


