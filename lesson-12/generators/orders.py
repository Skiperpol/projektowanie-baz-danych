from bson import ObjectId
from faker import Faker
from config import get_db, to_decimal
from datetime import datetime, timedelta
import random

fake = Faker('pl_PL')

def generate_orders(count, user_ids, product_ids):
    """Generate orders collection"""
    db = get_db()
    orders = []
    
    if not user_ids:
        print("No users found. Please generate users first.")
        return []
    
    if not product_ids:
        print("No products found. Please generate products first.")
        return []
    
    # Get users with addresses
    users = list(db.users.find({"_id": {"$in": user_ids}, "addresses": {"$exists": True, "$ne": []}}))
    
    if not users:
        print("No users with addresses found.")
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
    
    for i in range(count):
        user = random.choice(users)
        user_id = user["_id"]
        
        # Get user addresses
        addresses = user.get("addresses", [])
        if not addresses:
            continue
        
        shipping_address_obj = next((a for a in addresses if a.get("is_default_shipping")), addresses[0])
        billing_address_obj = random.choice(addresses)
        
        shipping_address = {
            "street": shipping_address_obj.get("street", fake.street_address()),
            "city": shipping_address_obj.get("city", fake.city()),
            "postal_code": shipping_address_obj.get("postal_code", fake.postcode()),
            "country": shipping_address_obj.get("country", "PL")
        }
        
        billing_address = {
            "street": billing_address_obj.get("street", fake.street_address()),
            "city": billing_address_obj.get("city", fake.city()),
            "postal_code": billing_address_obj.get("postal_code", fake.postcode()),
            "country": billing_address_obj.get("country", "PL")
        }
        
        # Get products
        products = list(db.products.find({"_id": {"$in": product_ids}}))
        if not products:
            continue
        
        # Order items (1-5 items)
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, k=min(num_items, len(products)))
        
        items = []
        total_amount = 0.0
        
        for product in selected_products:
            if not product.get("variants"):
                continue
            
            variant = random.choice(product["variants"])
            quantity = random.randint(1, 3)
            
            # Get price (promotion price if available, otherwise base price)
            if variant.get("current_promotion"):
                unit_price = float(variant["current_promotion"]["final_price"])
            else:
                unit_price = float(variant["base_price"])
            
            item_total = unit_price * quantity
            total_amount += item_total
            
            # Get color for product name
            color = variant.get("attributes", {}).get("color", "")
            product_name = f"{product['name']}"
            if color:
                product_name += f" ({color})"
            
            item = {
                "product_id": product["_id"],
                "variant_sku": variant.get("sku", ""),
                "name": product_name,
                "quantity": quantity,
                "unit_price": to_decimal(unit_price)
            }
            items.append(item)
        
        if not items:
            continue
        
        # Add delivery cost
        delivery_method = random.choice(delivery_methods)
        total_amount += delivery_method["cost"]
        
        status = random.choices(statuses, weights=status_weights)[0]
        order_date = datetime.now() - timedelta(days=random.randint(0, 180))
        
        order = {
            "_id": ObjectId(),
            "user_id": user_id,
            "status": status,
            "order_date": order_date,
            "shipping_address": shipping_address,
            "billing_address": billing_address,
            "delivery_method": {
                "name": delivery_method["name"],
                "cost": to_decimal(delivery_method["cost"])
            },
            "payment_method": random.choice(payment_methods),
            "total_amount": to_decimal(round(total_amount, 2)),
            "items": items
        }
        orders.append(order)
    
    if orders:
        db.orders.insert_many(orders)
        print(f"Generated {len(orders)} orders")
        return [o["_id"] for o in orders]
    return []
