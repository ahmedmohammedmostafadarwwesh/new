# عبدالله محمد عادل
"""Utility to seed the MongoDB dashboard collection with example rows."""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dashboard_db")

async def seed():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db["rows"]
    # drop for clean start
    # here add data and refresh by  cd backend
#    venv\Scripts\activate
#    python seed.py
# http://localhost:8000/Dashboard/Dashboard.html
    await collection.drop()
    sample = [
        {"id": 1, "name": "Ahmed Hassan",     "col1": "Sales North",  "col2": "Q1 2026", "col3": "Complete",    "col4": "85%", "col5": "92%", "col6": "5%"},
        {"id": 2, "name": "Fatima Al-Rashid", "col1": "Marketing Team","col2": "Q1 2026", "col3": "In Progress", "col4": "65%", "col5": "78%", "col6": "15%"},
        {"id": 3, "name": "Mohammed Ali",     "col1": "Dev Frontend", "col2": "Q1 2026", "col3": "Complete",    "col4": "95%", "col5": "88%", "col6": "3%"},
        {"id": 4, "name": "Layla Noor",       "col1": "Design UX",    "col2": "Q1 2026", "col3": "In Progress", "col4": "72%", "col5": "85%", "col6": "12%"},
        {"id": 5, "name": "Omar Khalil",      "col1": "Backend API",  "col2": "Q1 2026", "col3": "At Risk",     "col4": "55%", "col5": "65%", "col6": "28%"},
        {"id": 6, "name": "Sara Youssef",     "col1": "QA Team",      "col2": "Q1 2026", "col3": "Pending",     "col4": "40%", "col5": "50%", "col6": "10%"},
        {"id": 7, "name": "Yasir Khan",       "col1": "Support",      "col2": "Q1 2026", "col3": "Complete",    "col4": "90%", "col5": "85%", "col6": "2%"},
        {"id": 8, "name": "Noura Al-Mansoori", "col1": "Dev Backend",  "col2": "Q1 2026", "col3": "Complete",    "col4": "98%", "col5": "95%", "col6": "1%"},

    ]
    await collection.insert_many(sample)
    print("Inserted 8 sample rows")

if __name__ == "__main__":
    asyncio.run(seed())
