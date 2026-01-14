import random
from bson import ObjectId
from datetime import datetime

def generate_review():
    return {
        "_id": ObjectId(),
        "product_id": ObjectId(),
        "user_id": ObjectId(),
        "rating": random.randint(1, 5),
        "comment": "Bardzo dobry produkt!",
        "helpful_votes": random.randint(0, 20),
        "posted_at": datetime.utcnow()
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_review())
