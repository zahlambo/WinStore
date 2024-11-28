import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import asyncio  # For async setup

load_dotenv()

# Get MongoDB credentials from environment variables
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]

async def initialize_indexes():
    """
    Ensure unique indexes for username and Email.
    This function should be called during application startup.
    """
    await db['User'].create_index("username", unique=True)
    await db['User'].create_index("Email", unique=True)

def getDatabase():
    return db

# Example of calling the index creation (e.g., in FastAPI `on_startup`)
if __name__ == "__main__":
    asyncio.run(initialize_indexes())
