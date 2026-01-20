import random
from bson import ObjectId
from datetime import datetime, timedelta

def generate_promotion():
    start = datetime.utcnow()
    end = start + timedelta(days=random.randint(1, 30))
    return {
        "_id": ObjectId(),
        "name": "PromocjaX",
        "is_active": True,
        "start_date": start,
        "end_date": end,
        "discount": {
            "type": "percent",
            "value": random.randint(5, 50)
        },
        "target": {
            "scope": "product",
            "target_id": ObjectId()
        }
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_promotion())
