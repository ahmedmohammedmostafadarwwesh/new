# عبدالله محمد عادل
"""Utility to insert a single row into the dashboard collection."""
import sys
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dashboard_db")

async def insert(row):
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    await db["rows"].insert_one(row)
    print("Inserted:", row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_row.py '{\"id\":6,\"name\":\"XYZ\",...}'")
        sys.exit(1)
    import json
    try:
        row = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        print("Invalid JSON")
        sys.exit(1)
    import asyncio
    asyncio.run(insert(row))
