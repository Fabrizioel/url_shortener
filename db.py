from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Initiliaze client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Test connection
try:
    client.admin.command('ping')
    print(f"✅ Successfully connected to MongoDB: {DB_NAME}")
except Exception as e:
    print("❌ Connection failed:", e)