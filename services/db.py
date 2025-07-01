from pymongo import MongoClient
from config.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["ai_campaign"]
messages_collection = db["messages"]

def save_message(data):
    messages_collection.insert_one(data)