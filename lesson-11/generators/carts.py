import random
from bson import ObjectId
from datetime import datetime

def generate_cart():
    return {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "updated_at": datetime.utcnow(),
        "items": [
            {
                "product_id": ObjectId(),
                "variant_id": ObjectId(),
                "quantity": random.randint(1, 5)
            }
            for _ in range(random.randint(1, 3))
        ]
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_cart())
