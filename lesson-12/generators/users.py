from bson import ObjectId
from faker import Faker
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
import random
import hashlib

fake = Faker('pl_PL')


def generate_password_hash(password):
    """Simple password hash (in production use bcrypt)"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_users(count):
    """Generate users collection"""
    db = get_db()
    users = []
    
    roles = ['customer', 'admin', 'warehouse_staff', 'support']
    
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}.{i}@{fake.domain_name()}"
        password = fake.password(length=12)
        
        num_addresses = random.randint(1, 3)
        addresses = []
        for j in range(num_addresses):
            address = {
                "id": ObjectId(),
                "street": fake.street_address(),
                "city": fake.city(),
                "postal_code": fake.postcode(),
                "country": "PL",
                "is_default_shipping": j == 0,
                "phone": fake.phone_number()
            }
            addresses.append(address)
        
        user = {
            "_id": ObjectId(),
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password_hash": generate_password_hash(password),
            "registered_at": fake.date_time_between(start_date='-2y', end_date='now'),
            "roles": random.sample(roles, k=random.randint(1, 2)) if random.random() > 0.9 else ['customer'],
            "addresses": addresses
        }
        users.append(user)
    
    if users:
        insert_in_batches(db.users, users, batch_size=2000)
        print(f"Generated {len(users)} users")
        return [u["_id"] for u in users]
    return []
