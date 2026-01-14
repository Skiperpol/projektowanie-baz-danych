from bson import ObjectId
from bson.decimal128 import Decimal128
from faker import Faker
from config import get_db, to_decimal, insert_in_batches
from datetime import datetime, timedelta
import random

fake = Faker('pl_PL')

def generate_orders(count, user_ids, product_ids):
    db = get_db()
    
    print("Ładowanie danych do pamięci...")
    users = list(db.users.find(
        {"_id": {"$in": user_ids}, "addresses": {"$exists": True, "$ne": []}},
        {"_id": 1, "addresses": 1}
    ))
    
    products = list(db.products.find(
        {"_id": {"$in": product_ids}},
        {"_id": 1, "name": 1, "variants": 1}
    ))

    if not users or not products:
        print("Brak użytkowników lub produktów.")
        return []

    statuses = ['new', 'payment_pending', 'processing', 'shipped', 'completed', 'cancelled']
    status_weights = [0.1, 0.1, 0.2, 0.2, 0.35, 0.05]
    delivery_methods = [
        {"name": "Kurier DHL", "cost": 15.99},
        {"name": "Kurier InPost", "cost": 12.99},
        {"name": "Paczkomat", "cost": 9.99},
        {"name": "Odbiór osobisty", "cost": 0.00},
        {"name": "Poczta Polska", "cost": 8.99}
    ]
    payment_methods = ["BLIK", "Karta kredytowa", "Przelew", "PayPal", "Gotówka przy odbiorze"]
    
    orders = []
    
    print(f"Generowanie {count} dokumentów...")
    for _ in range(count):
        user = random.choice(users)
        addresses = user.get("addresses", [])
        
        def clean_address(addr_obj):
            return {
                "city": addr_obj.get("city", "Nieznane"),
                "country": addr_obj.get("country", "PL"),
                "postal_code": addr_obj.get("postal_code", "00-000"),
                "street": addr_obj.get("street", "Brak ulicy")
            }

        shipping_raw = next((a for a in addresses if a.get("is_default_shipping")), addresses[0])
        billing_raw = random.choice(addresses)

        shipping_address = clean_address(shipping_raw)
        billing_address = clean_address(billing_raw)
        
        num_items = random.randint(1, 5)
        selected_prods = random.sample(products, k=min(num_items, len(products)))
        
        items = []
        total_amount = 0.0
        
        for prod in selected_prods:
            if not prod.get("variants"): continue
            
            variant = random.choice(prod["variants"])
            quantity = random.randint(1, 3)
            
            raw_price = variant.get("current_promotion", {}).get("final_price") or variant["base_price"]
            unit_price = float(raw_price.to_decimal()) if isinstance(raw_price, Decimal128) else float(raw_price)
            
            total_amount += (unit_price * quantity)
            
            items.append({
                "product_id": prod["_id"],
                "variant_sku": str(variant.get("sku", "N/A")),
                "name": f"{prod['name']} ({variant.get('attributes', {}).get('color', 'N/A')})",
                "quantity": int(quantity),
                "unit_price": to_decimal(unit_price)
            })

        if not items: continue

        delivery = random.choice(delivery_methods)
        
        order = {
            "_id": ObjectId(),
            "user_id": user["_id"],
            "status": random.choices(statuses, weights=status_weights)[0],
            "order_date": datetime.now() - timedelta(days=random.randint(0, 180)),
            "shipping_address": shipping_address,
            "billing_address": billing_address,
            "delivery_method": {
                "name": delivery["name"],
                "cost": to_decimal(delivery["cost"])
            },
            "payment_method": random.choice(payment_methods),
            "total_amount": to_decimal(round(total_amount + delivery["cost"], 2)),
            "items": items
        }
        orders.append(order)

    if orders:
        print(f"Wysyłanie {len(orders)} zamówień do bazy...")
        insert_in_batches(db.orders, orders, batch_size=2000)
        return [o["_id"] for o in orders]
    
    return []
