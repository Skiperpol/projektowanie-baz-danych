from bson import ObjectId
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
import random


def generate_carts(count, user_ids, product_ids):
    """Generate carts collection"""
    db = get_db()
    carts = []
    
    if not user_ids:
        print("No users found. Please generate users first.")
        return []
    
    if not product_ids:
        print("No products found. Please generate products first.")
        return []
    
    products = list(db.products.find({"_id": {"$in": product_ids}}))
    
    users_with_carts = random.sample(user_ids, k=min(count, len(user_ids)))
    
    for user_id in users_with_carts:
        num_items = random.randint(1, 5)
        items = []
        
        selected_products = random.sample(products, k=min(num_items, len(products)))
        
        for product in selected_products:
            if not product.get("variants"):
                continue
            
            variant = random.choice(product["variants"])
            quantity = random.randint(1, 3)
            
            item = {
                "product_id": product["_id"],
                "variant_id": variant["_id"],
                "quantity": quantity
            }
            items.append(item)
        
        if items:
            cart = {
                "_id": ObjectId(),
                "user_id": user_id,
                "items": items,
                "updated_at": datetime.now() - timedelta(days=random.randint(0, 30))
            }
            carts.append(cart)
    
    if carts:
        insert_in_batches(db.carts, carts, batch_size=2000)
        print(f"Generated {len(carts)} carts")
        return [c["_id"] for c in carts]
    return []
