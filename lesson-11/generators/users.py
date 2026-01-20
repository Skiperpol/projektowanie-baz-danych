import random
from bson import ObjectId
from datetime import datetime

def generate_user():
    return {
        "_id": ObjectId(),
        "email": f"user{random.randint(1,1000)}@example.com",
        "first_name": "Jan",
        "last_name": "Kowalski",
        "password_hash": "hash",
        "registered_at": datetime.utcnow(),
        "roles": [random.choice(["customer", "admin", "warehouse_staff", "support"])],
        "addresses": [
            {
                "id": ObjectId(),
                "street": "Ulica 3",
                "city": "Miasto",
                "postal_code": "00-000",
                "country": "PL",
                "is_default_shipping": True,
                "phone": "123456789"
            }
        ]
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_user())
