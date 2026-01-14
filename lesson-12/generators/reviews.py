from bson import ObjectId
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
from pymongo.errors import PyMongoError
import random

from pymongo import UpdateOne

def generate_reviews(count, user_ids, product_ids):
    """Błyskawiczne generowanie opinii"""
    db = get_db()
    reviews = []
    
    if not user_ids or not product_ids:
        print("Błąd: Brak ID użytkowników lub produktów.")
        return []

    pos = ["Świetny produkt, polecam!", "Bardzo dobra jakość.", "Doskonały zakup!"]
    neg = ["Nie spełnia oczekiwań.", "Dostawa trwała zbyt długo.", "Słaba jakość."]
    
    print(f"Generowanie {count} dokumentów opinii w pamięci...")
    for _ in range(count):
        rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.15, 0.3, 0.4])[0]
        
        if rating >= 4: comment = random.choice(pos)
        elif rating <= 2: comment = random.choice(neg)
        else: comment = random.choice(pos + neg)

        reviews.append({
            "_id": ObjectId(),
            "product_id": random.choice(product_ids),
            "user_id": random.choice(user_ids),
            "rating": int(rating),
            "comment": comment,
            "helpful_votes": random.randint(0, 50) if rating >= 4 else random.randint(0, 10),
            "posted_at": datetime.now() - timedelta(days=random.randint(0, 365))
        })
    
    if reviews:
        try:
            print(f"Wysyłanie {len(reviews)} opinii do bazy...")
            insert_in_batches(db.reviews, reviews, batch_size=5000)
            
            update_product_reviews_fast(db, product_ids)

            return [r["_id"] for r in reviews]
        except PyMongoError as e:
            print("Błąd zapisu:", e)
            return []
    return []


def update_product_reviews_fast(db, product_ids):
    """Aktualizacja statystyk za pomocą agregacji i bulk_write"""
    print("Obliczanie średnich ocen (Agregacja)...")
    
    pipeline = [
        {"$match": {"product_id": {"$in": product_ids}}},
        {"$group": {
            "_id": "$product_id",
            "review_count": {"$sum": 1},
            "avg_rating": {"$avg": "$rating"}
        }}
    ]
    
    results = db.reviews.aggregate(pipeline)
    
    updates = []
    from config import to_decimal
    
    for res in results:
        updates.append(UpdateOne(
            {"_id": res["_id"]},
            {"$set": {
                "review_count": res["review_count"],
                "avg_rating": to_decimal(round(res["avg_rating"], 1))
            }}
        ))
    
    if updates:
        print(f"Aktualizacja {len(updates)} produktów...")
        db.products.bulk_write(updates)