import random
from bson import ObjectId
from datetime import datetime

def generate_user_favorite():
    return {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "product_id": ObjectId(),
        "variant_id": ObjectId(),
        "added_at": datetime.utcnow()
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_user_favorite())
