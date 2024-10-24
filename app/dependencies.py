# app/dependencies.py

from pymongo import MongoClient
import os

def get_mongo_client() -> MongoClient:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    return client

