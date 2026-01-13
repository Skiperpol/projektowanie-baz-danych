from bson import ObjectId
from config import get_db
from datetime import datetime, timedelta
import random

def generate_reviews(count, user_ids, product_ids):
    """Generate reviews collection"""
    db = get_db()
    reviews = []
    
    if not user_ids:
        print("No users found. Please generate users first.")
        return []
    
    if not product_ids:
        print("No products found. Please generate products first.")
        return []
    
    # Get products
    products = list(db.products.find({"_id": {"$in": product_ids}}))
    
    if not products:
        print("No products found.")
        return []
    
    # Comments templates
    positive_comments = [
        "Świetny produkt, polecam!",
        "Bardzo dobra jakość, szybka dostawa.",
        "Spełnia wszystkie moje oczekiwania.",
        "Doskonały stosunek jakości do ceny.",
        "Kupiłbym ponownie bez wahania.",
        "Produkt zgodny z opisem, wszystko działa perfekcyjnie.",
        "Bardzo zadowolony z zakupu.",
        "Polecam wszystkim znajomym."
    ]
    
    negative_comments = [
        "Nie spełnia oczekiwań, jakość mogłaby być lepsza.",
        "Dostawa trwała zbyt długo.",
        "Produkt działa, ale ma kilka wad.",
        "Można było lepiej za tę cenę."
    ]
    
    # Generate reviews
    for i in range(count):
        user_id = random.choice(user_ids)
        product = random.choice(products)
        product_id = product["_id"]
        
        # Rating distribution: more positive reviews
        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.05, 0.1, 0.15, 0.3, 0.4]
        )[0]
        
        # Comment based on rating
        if rating >= 4:
            comment = random.choice(positive_comments)
        elif rating <= 2:
            comment = random.choice(negative_comments)
        else:
            comment = random.choice(positive_comments + negative_comments)
        
        # Add some variation to comments
        if random.random() < 0.3:
            comment += " " + "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        
        helpful_votes = random.randint(0, 50) if rating >= 4 else random.randint(0, 10)
        posted_at = datetime.now() - timedelta(days=random.randint(0, 365))
        
        review = {
            "_id": ObjectId(),
            "product_id": product_id,
            "user_id": user_id,
            "rating": rating,
            "comment": comment[:2000],  # Max length from validation
            "helpful_votes": helpful_votes,
            "posted_at": posted_at
        }
        reviews.append(review)
    
    if reviews:
        db.reviews.insert_many(reviews)
        print(f"Generated {len(reviews)} reviews")
        
        # Update product review counts and avg_rating
        update_product_reviews(db, product_ids)
        
        return [r["_id"] for r in reviews]
    return []

def update_product_reviews(db, product_ids):
    """Update product review_count and avg_rating based on actual reviews"""
    products = list(db.products.find({"_id": {"$in": product_ids}}))
    
    for product in products:
        product_reviews = list(db.reviews.find({"product_id": product["_id"]}))
        
        if product_reviews:
            review_count = len(product_reviews)
            avg_rating = sum(r["rating"] for r in product_reviews) / review_count
            
            from config import to_decimal
            db.products.update_one(
                {"_id": product["_id"]},
                {
                    "$set": {
                        "review_count": review_count,
                        "avg_rating": to_decimal(round(avg_rating, 1))
                    }
                }
            )
