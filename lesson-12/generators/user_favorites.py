from bson import ObjectId
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
import random


def generate_user_favorites(count, user_ids, product_ids):
    """Błyskawiczne generowanie ulubionych"""
    db = get_db()
    
    print("Ładowanie wariantów produktów do pamięci...")
    product_data = list(db.products.find(
        {"_id": {"$in": product_ids}},
        {"_id": 1, "variants._id": 1}
    ))
    
    if not product_data:
        print("Brak produktów.")
        return []

    prod_to_variants = {
        p["_id"]: [v["_id"] for v in p.get("variants", [])] 
        for p in product_data
    }
    available_prod_ids = list(prod_to_variants.keys())

    favorites = []
    favorite_pairs = set()
    
    print(f"Generowanie {count} dokumentów ulubionych...")
    
    max_attempts = count * 2 
    attempts = 0

    while len(favorites) < count and attempts < max_attempts:
        attempts += 1
        user_id = random.choice(user_ids)
        product_id = random.choice(available_prod_ids)
        
        pair = (user_id, product_id)
        if pair in favorite_pairs:
            continue
        
        favorite_pairs.add(pair)
        
        variant_list = prod_to_variants[product_id]
        variant_id = random.choice(variant_list) if variant_list else None
        
        favorite = {
            "_id": ObjectId(),
            "user_id": user_id,
            "product_id": product_id,
            "added_at": datetime.now() - timedelta(days=random.randint(0, 365))
        }
        
        if variant_id:
            favorite["variant_id"] = variant_id
            
        favorites.append(favorite)

    if favorites:
        print(f"Wysyłanie {len(favorites)} rekordów do bazy...")
        insert_in_batches(db.user_favorites, favorites, batch_size=5000)
        return [f["_id"] for f in favorites]
    
    return []