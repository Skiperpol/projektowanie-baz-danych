from bson import ObjectId
from faker import Faker
from config import get_db, insert_in_batches
import random

fake = Faker('pl_PL')


def generate_warehouses(count):
    """Generate warehouses collection"""
    db = get_db()
    warehouses = []
    
    warehouse_types = ['central', 'local', 'pickup_point']
    cities = ['Warszawa', 'Kraków', 'Gdańsk', 'Wrocław', 'Poznań', 'Łódź']
    
    for i in range(count):
        warehouse_type = random.choice(warehouse_types)
        city = cities[i % len(cities)] if i < len(cities) else fake.city()
        
        warehouse = {
            "_id": ObjectId(),
            "name": f"Magazyn {warehouse_type.capitalize()} - {city}",
            "type": warehouse_type,
            "is_active": random.choice([True, True, False]),
            "address": {
                "street": fake.street_address(),
                "city": city,
                "postal_code": fake.postcode(),
                "country": "PL"
            }
        }
        
        if random.random() > 0.3:
            warehouse["location"] = {
                "type": "Point",
                "coordinates": [
                    float(fake.longitude()),
                    float(fake.latitude())
                ]
            }
        
        warehouses.append(warehouse)
    
    if warehouses:
        insert_in_batches(db.warehouses, warehouses, batch_size=2000)
        print(f"Generated {len(warehouses)} warehouses")
        return [w["_id"] for w in warehouses]
    return []
