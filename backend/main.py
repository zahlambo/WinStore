from fastapi import FastAPI
from db import get_database
import json
from model import *
import re

app = FastAPI()
db = get_database()
collection = db["apps"]


@app.post("/add_item", response_model=str)
async def add_item(item: AddItem):
    # Insert the new item into the database
    await collection.insert_one(item.model_dump())
    return "Item added successfully!"


@app.get("/get_all_items")
async def get_all_items():
    items = await collection.find({}, {"_id": 0}).to_list()
    return items


@app.get("/items/{appquery}", response_model=str)
async def read_item(items: str):
    winget_script = "winget install "
    for i in items.split(","):
        # Removing spaces from the string
        i = i.strip().replace(" ", "")
        item = await collection.find_one({"name": re.compile(i, re.IGNORECASE)})
        if item:
            winget_script += item['ID'] + " "
    return winget_script
