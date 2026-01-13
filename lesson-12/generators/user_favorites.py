from bson import ObjectId
from config import get_db
from datetime import datetime, timedelta
import random

def generate_user_favorites(count, user_ids, product_ids):
    """Generate user_favorites collection"""
    db = get_db()
    favorites = []
    
    if not user_ids:
        print("No users found. Please generate users first.")
        return []
    
    if not product_ids:
        print("No products found. Please generate products first.")
        return []
    
    # Get products with variants
    products = list(db.products.find({"_id": {"$in": product_ids}}))
    
    if not products:
        print("No products found.")
        return []
    
    # Create favorites (not all users have favorites, some have multiple)
    favorite_pairs = set()  # To avoid duplicates
    
    for i in range(count):
        user_id = random.choice(user_ids)
        product = random.choice(products)
        product_id = product["_id"]
        
        # Check for duplicate
        pair = (user_id, product_id)
        if pair in favorite_pairs:
            continue
        favorite_pairs.add(pair)
        
        # Get variant if available (optional field)
        variant_id = None
        if product.get("variants"):
            variant = random.choice(product["variants"])
            variant_id = variant["_id"]
        
        added_at = datetime.now() - timedelta(days=random.randint(0, 365))
        
        favorite = {
            "_id": ObjectId(),
            "user_id": user_id,
            "product_id": product_id,
            "added_at": added_at
        }
        
        if variant_id:
            favorite["variant_id"] = variant_id
        
        favorites.append(favorite)
    
    if favorites:
        db.user_favorites.insert_many(favorites)
        print(f"Generated {len(favorites)} user favorites")
        return [f["_id"] for f in favorites]
    return []
