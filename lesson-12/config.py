import os
from pymongo import MongoClient
from bson import Decimal128
from datetime import datetime
import json

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'ecommerce_db')

# Load document counts
def load_counts():
    """Load document counts from counts.json"""
    with open('counts.json', 'r') as f:
        return json.load(f)

# Initialize MongoDB client
def get_db():
    """Get MongoDB database connection"""
    client = MongoClient(MONGO_URI)
    return client[DATABASE_NAME]

# Helper function to convert float to Decimal128
def to_decimal(value):
    """Convert float to Decimal128 for MongoDB"""
    return Decimal128(str(value))
