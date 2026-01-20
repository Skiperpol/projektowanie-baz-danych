
# --- NOWY GENERATOR: duże ilości losowych danych ---
import os
import json
import random
from faker import Faker
from pymongo import MongoClient
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'row_counts.json')
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGO_DB', 'shopdb')
BATCH_SIZE = 1000

fake = Faker('pl_PL')

def gen_warehouse(_id):
    return {
        "_id": f"wh_{_id}",
        "name": f"Magazyn {_id} - {fake.city()}",
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "postal_code": fake.postcode(),
            "country": "PL"
        },
        "is_active": True
    }

def gen_manufacturer(_id):
    return {
        "_id": _id,
        "name": fake.company(),
        "description": fake.text(50),
        "website": fake.url(),
        "contact": {
            "email": fake.company_email(),
            "phone": fake.phone_number()
        },
        "active": True
    }

def gen_user(_id):
    return {
        "_id": f"user_{_id}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "password_hash": fake.sha256(),
        "roles": ["user"],
        "addresses": [
            {
                "id": f"addr_{_id}",
                "street": fake.street_address(),
                "city": fake.city(),
                "postal_code": fake.postcode(),
                "country": "PL",
                "is_default_shipping": True
            }
        ],
        "registered_at": fake.date_time_between(start_date='-2y', end_date='now'),
    }

def gen_product(_id, manufacturer, categories, variants):
    return {
        "_id": f"prod_{_id}",
        "name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "description": fake.text(60),
        "manufacturer": manufacturer,
        "categories": categories,
        "base_attributes": {
            "warranty": "24 miesiące",
            "connection": "Bluetooth 5.0"
        },
        "avg_rating": round(random.uniform(3.5, 5.0), 1),
        "review_count": random.randint(0, 200),
        "variants": variants
    }

def gen_variant(_id, product_id, color, base_price, promo=None):
    v = {
        "_id": f"var_{_id}",
        "sku": f"SKU-{_id:06d}",
        "base_price": base_price,
        "attributes": {"color": color},
        "inventory_type": "bulk",
        "product_id": product_id
    }
    if promo:
        v["current_promotion"] = promo
    return v

def gen_inventory_bulk(warehouse_id, variant_id):
    return {
        "warehouse_id": warehouse_id,
        "variant_id": variant_id,
        "quantity_on_hand": random.randint(10, 200),
        "quantity_reserved": random.randint(0, 10)
    }

def gen_cart(user_id, variant_id, product_id):
    return {
        "user_id": user_id,
        "updated_at": fake.date_time_between(start_date='-1y', end_date='now'),
        "items": [
            {
                "variant_id": variant_id,
                "product_id": product_id,
                "quantity": random.randint(1, 3)
            }
        ]
    }

def gen_order(_id, user_id, shipping_address, billing_address, items):
    return {
        "_id": f"order_{_id}",
        "user_id": user_id,
        "status": "PAID",
        "order_date": fake.date_time_between(start_date='-1y', end_date='now'),
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "delivery_method": {
            "name": "Kurier DHL",
            "cost": round(random.uniform(10, 30), 2)
        },
        "payment_method": random.choice(["BLIK", "KARTA", "PRZELEW"]),
        "total_amount": sum(i["unit_price"] for i in items),
        "items": items
    }

def gen_review(product_id, user_id):
    return {
        "product_id": product_id,
        "user_id": user_id,
        "rating": random.randint(4, 5),
        "comment": fake.sentence(),
        "posted_at": fake.date_time_between(start_date='-1y', end_date='now'),
        "helpful_votes": random.randint(0, 20)
    }

def gen_promotion(_id, target_id):
    return {
        "_id": f"promo_{_id}",
        "name": fake.catch_phrase(),
        "is_active": True,
        "start_date": fake.date_time_between(start_date='-2y', end_date='-1y'),
        "end_date": fake.date_time_between(start_date='-1y', end_date='now'),
        "target": {
            "scope": "CATEGORY",
            "target_id": target_id
        },
        "discount": {
            "type": "PERCENTAGE",
            "value": random.randint(5, 30)
        }
    }

def main():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        row_counts = json.load(f)

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Warehouses
    warehouses = [gen_warehouse(i) for i in range(row_counts['warehouses'])]
    db.warehouses.delete_many({})
    for i in range(0, len(warehouses), BATCH_SIZE):
        db.warehouses.insert_many(warehouses[i:i+BATCH_SIZE])

    # Manufacturers
    manufacturers = [gen_manufacturer(i) for i in range(row_counts['manufacturers'])]
    db.manufacturers.delete_many({})
    for i in range(0, len(manufacturers), BATCH_SIZE):
        db.manufacturers.insert_many(manufacturers[i:i+BATCH_SIZE])

    # Users
    users = [gen_user(i) for i in range(row_counts['users'])]
    db.users.delete_many({})
    for i in range(0, len(users), BATCH_SIZE):
        db.users.insert_many(users[i:i+BATCH_SIZE])

    # Promotions
    promotions = [gen_promotion(i, random.randint(1, 10)) for i in range(row_counts['promotions'])]
    db.promotions.delete_many({})
    for i in range(0, len(promotions), BATCH_SIZE):
        db.promotions.insert_many(promotions[i:i+BATCH_SIZE])

    # Products & Variants
    categories = [
        {"id": 10, "name": "Audio"},
        {"id": 20, "name": "Elektronika"}
    ]
    products = []
    variants = []
    for i in range(row_counts['products']):
        man = random.choice(manufacturers)
        prod_variants = []
        for v in range(2):
            var_id = i * 2 + v
            promo = random.choice(promotions) if random.random() < 0.2 else None
            variant = gen_variant(var_id, f"prod_{i}", random.choice(["Black", "Silver", "Red", "Blue"]), round(random.uniform(100, 2000), 2), promo)
            variants.append(variant)
            prod_variants.append(variant)
        products.append(gen_product(i, {"id": man["_id"], "name": man["name"]}, categories, prod_variants))
    db.products.delete_many({})
    for i in range(0, len(products), BATCH_SIZE):
        db.products.insert_many(products[i:i+BATCH_SIZE])
    db.variants.delete_many({})
    for i in range(0, len(variants), BATCH_SIZE):
        db.variants.insert_many(variants[i:i+BATCH_SIZE])

    # Inventory bulk
    inventory_bulk = [gen_inventory_bulk(random.choice(warehouses)["_id"], v["_id"]) for v in variants[:row_counts['inventory_bulk']]]
    db.inventory_bulk.delete_many({})
    for i in range(0, len(inventory_bulk), BATCH_SIZE):
        db.inventory_bulk.insert_many(inventory_bulk[i:i+BATCH_SIZE])

    # Carts
    carts = [gen_cart(random.choice(users)["_id"], random.choice(variants)["_id"], random.choice(products)["_id"]) for _ in range(row_counts['carts'])]
    db.carts.delete_many({})
    for i in range(0, len(carts), BATCH_SIZE):
        db.carts.insert_many(carts[i:i+BATCH_SIZE])

    # Orders
    orders = []
    for i in range(row_counts['orders']):
        user = random.choice(users)
        items = [{
            "product_id": random.choice(products)["_id"],
            "variant_sku": random.choice(variants)["sku"],
            "name": fake.word().capitalize(),
            "quantity": random.randint(1, 3),
            "unit_price": round(random.uniform(100, 2000), 2)
        } for _ in range(random.randint(1, 3))]
        orders.append(gen_order(i, user["_id"], user["addresses"][0], user["addresses"][0], items))
    db.orders.delete_many({})
    for i in range(0, len(orders), BATCH_SIZE):
        db.orders.insert_many(orders[i:i+BATCH_SIZE])

    # Reviews
    reviews = [gen_review(random.choice(products)["_id"], random.choice(users)["_id"]) for _ in range(row_counts['reviews'])]
    db.reviews.delete_many({})
    for i in range(0, len(reviews), BATCH_SIZE):
        db.reviews.insert_many(reviews[i:i+BATCH_SIZE])

    print("Wygenerowano dane do MongoDB!")

if __name__ == "__main__":
    main()
