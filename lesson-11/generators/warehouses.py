import random
from bson import ObjectId

def generate_warehouse():
    return {
        "_id": ObjectId(),
        "name": "MagazynX",
        "type": random.choice(["central", "local", "pickup_point"]),
        "is_active": True,
        "address": {
            "street": "Ulica 4",
            "city": "Miasto",
            "postal_code": "00-000",
            "country": "PL"
        },
        "location": {
            "type": "Point",
            "coordinates": [random.uniform(14, 24), random.uniform(50, 54)]
        }
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_warehouse())
