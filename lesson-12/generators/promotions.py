from bson import ObjectId
from bson.decimal128 import Decimal128
from faker import Faker
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
import random

fake = Faker('pl_PL')

def generate_promotions(count, product_ids, category_ids):
    """Generate promotions collection"""
    db = get_db()
    promotions = []
    
    promotion_names = [
        "Zimowa Wyprzedaż",
        "Wiosenna Promocja",
        "Letnie Oferty",
        "Black Friday",
        "Cyber Monday",
        "Wielkanocna Promocja",
        "Dzień Dziecka",
        "Powrót do Szkoły"
    ]
    
    discount_types = ["PERCENTAGE", "FIXED"]
    scopes = ["SINGLE_PRODUCT", "CATEGORY", "MANUFACTURER", "ALL"]
    
    for i in range(count):
        name = promotion_names[i % len(promotion_names)] if i < len(promotion_names) else f"Promocja {i+1}"
        
        days_offset = random.randint(-60, 60)
        start_date = datetime.now() + timedelta(days=days_offset)
        end_date = start_date + timedelta(days=random.randint(7, 30))
        
        discount_type = random.choice(discount_types)
        if discount_type == "PERCENTAGE":
            value = random.randint(5, 50)
        else:
            value = random.randint(10, 500)
        
        scope = random.choice(scopes)
        
        if scope == "SINGLE_PRODUCT" and product_ids:
            target_id = random.choice(product_ids)
        elif scope == "CATEGORY" and category_ids:
            target_id = random.choice(category_ids)
        elif scope == "MANUFACTURER":
            manufacturers = db.manufacturers.find({}, {"_id": 1})
            manufacturer_list = [m["_id"] for m in manufacturers]
            target_id = random.choice(manufacturer_list) if manufacturer_list else ObjectId()
        else:
            target_id = ObjectId()
        
        promotion = {
            "_id": ObjectId(),
            "name": name,
            "is_active": start_date <= datetime.now() <= end_date,
            "start_date": start_date,
            "end_date": end_date,
            "target": {
                "scope": scope,
                "target_id": target_id
            },
            "discount": {
                "type": discount_type,
                "value": value
            }
        }
        promotions.append(promotion)
    
    if promotions:
        insert_in_batches(db.promotions, promotions, batch_size=2000)
        print(f"Generated {len(promotions)} promotions")

        apply_promotions_to_products(db, promotions, product_ids)

        return [p["_id"] for p in promotions]
    return []

def apply_promotions_to_products(db, promotions, product_ids):
    """Apply active promotions to product variants"""
    active_promotions = [p for p in promotions if p["is_active"]]
    
    if not active_promotions or not product_ids:
        return
    
    products = list(db.products.find({"_id": {"$in": product_ids}}))
    
    for product in products:
        for variant in product.get("variants", []):
            if random.random() < 0.2:
                promo = random.choice(active_promotions)

                raw_price = variant["base_price"]
                if isinstance(raw_price, Decimal128):
                    base_price = float(raw_price.to_decimal())
                else:
                    base_price = float(raw_price)
                
                if promo["discount"]["type"] == "PERCENTAGE":
                    discount = promo["discount"]["value"]
                    final_price = base_price * (1 - discount / 100)
                else:
                    final_price = max(0, base_price - promo["discount"]["value"])
                
                from config import to_decimal
                variant["current_promotion"] = {
                    "promo_id": promo["_id"],
                    "final_price": to_decimal(round(final_price, 2))
                }
        
        db.products.update_one(
            {"_id": product["_id"]},
            {"$set": {"variants": product["variants"]}}
        )
