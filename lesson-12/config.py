import os
from typing import Iterable, List
from pymongo import MongoClient
from bson import Decimal128
from datetime import datetime
import json

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'projektowanie-mongodb')


def load_counts():
    """Load document counts from counts.json"""
    with open('counts.json', 'r') as f:
        return json.load(f)


def get_db():
    """Get MongoDB database connection"""
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]


def to_decimal(value):
    """Convert float to Decimal128 for MongoDB"""
    return Decimal128(str(value))


def insert_in_batches(collection, documents: List[dict], batch_size: int = 2000):
    """
    Insert documents into MongoDB in batches to avoid 16MB limit.

    Parameters:
        collection: MongoDB collection
        documents: list of documents to insert
        batch_size: maximum number of documents per batch
    """
    if not documents:
        return

    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        if not batch:
            continue
        collection.insert_many(batch)
