from bson import ObjectId
from faker import Faker
from config import get_db
import random

fake = Faker('pl_PL')

def generate_manufacturers(count):
    """Generate manufacturers collection"""
    db = get_db()
    manufacturers = []
    
    manufacturer_names = [
        "Sony", "Samsung", "Apple", "LG", "Philips",
        "Panasonic", "Xiaomi", "Huawei", "Canon", "Nikon"
    ]
    
    for i in range(count):
        name = manufacturer_names[i % len(manufacturer_names)] if i < len(manufacturer_names) else fake.company()
        
        manufacturer = {
            "_id": ObjectId(),
            "name": name,
            "active": random.choice([True, True, True, False]),  # 75% active
            "description": fake.text(max_nb_chars=200),
            "website": f"https://www.{name.lower().replace(' ', '')}.com",
            "contact": {
                "email": f"contact@{name.lower().replace(' ', '')}.pl",
                "phone": fake.phone_number()
            },
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "zip_code": fake.postcode()
            }
        }
        manufacturers.append(manufacturer)
    
    if manufacturers:
        db.manufacturers.insert_many(manufacturers)
        print(f"Generated {len(manufacturers)} manufacturers")
        return [m["_id"] for m in manufacturers]
    return []
