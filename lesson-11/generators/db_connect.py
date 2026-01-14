from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "shopdbv2"

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

if __name__ == "__main__":
    db = get_db()
    print("Połączono z bazą:", db.name)
