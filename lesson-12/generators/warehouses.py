from bson import ObjectId
from faker import Faker
from config import get_db
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
            "is_active": random.choice([True, True, False]),  # 67% active
            "address": {
                "street": fake.street_address(),
                "city": city,
                "postal_code": fake.postcode(),
                "country": "PL"
            }
        }
        
        # Add location (GeoJSON) for some warehouses
        if random.random() > 0.3:  # 70% have location
            warehouse["location"] = {
                "type": "Point",
                "coordinates": [
                    float(fake.longitude()),
                    float(fake.latitude())
                ]
            }
        
        warehouses.append(warehouse)
    
    if warehouses:
        db.warehouses.insert_many(warehouses)
        print(f"Generated {len(warehouses)} warehouses")
        return [w["_id"] for w in warehouses]
    return []
