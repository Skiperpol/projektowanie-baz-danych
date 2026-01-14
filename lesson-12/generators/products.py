from bson import ObjectId
from faker import Faker
from config import get_db, to_decimal, insert_in_batches
import random

fake = Faker('pl_PL')

CATEGORIES = [
    {"id": ObjectId(), "name": "Audio"},
    {"id": ObjectId(), "name": "Elektronika"},
    {"id": ObjectId(), "name": "Komputery"},
    {"id": ObjectId(), "name": "Telefony"},
    {"id": ObjectId(), "name": "Fotografia"},
    {"id": ObjectId(), "name": "Gaming"},
    {"id": ObjectId(), "name": "Akcesoria"},
    {"id": ObjectId(), "name": "Smart Home"}
]

PRODUCT_TEMPLATES = [
    ("Słuchawki Bezprzewodowe", "Wysokiej klasy słuchawki z redukcją szumów", ["Black", "White", "Silver"]),
    ("Smartfon", "Nowoczesny smartfon z zaawansowanym aparatem", ["Black", "Blue", "White"]),
    ("Laptop", "Wydajny laptop do pracy i rozrywki", ["Silver", "Black", "Gray"]),
    ("Kamera", "Profesjonalna kamera cyfrowa", ["Black", "Silver"]),
    ("Głośnik", "Głośnik Bluetooth z doskonałym dźwiękiem", ["Black", "White", "Red", "Blue"]),
    ("Tablet", "Tablet z dużym ekranem", ["Silver", "Space Gray", "Gold"]),
    ("Smartwatch", "Inteligentny zegarek", ["Black", "Silver", "Rose Gold"]),
    ("Klawiatura", "Mechaniczna klawiatura gamingowa", ["Black", "White", "RGB"]),
    ("Mysz", "Precyzyjna mysz gamingowa", ["Black", "White", "Pink"]),
    ("Monitor", "Monitor 4K do pracy i gier", ["Black", "Silver"])
]

def generate_products(count, manufacturer_ids):
    """Generate products collection with variants"""
    db = get_db()
    products = []
    all_variants = []
    
    if not manufacturer_ids:
        print("No manufacturers found. Please generate manufacturers first.")
        return [], []
    
    for i in range(count):
        template = PRODUCT_TEMPLATES[i % len(PRODUCT_TEMPLATES)]
        product_name, description, colors = template
        
        manufacturer_id = random.choice(manufacturer_ids)
        manufacturer_doc = db.manufacturers.find_one({"_id": manufacturer_id})
        manufacturer_name = manufacturer_doc["name"] if manufacturer_doc else "Unknown"
        
        num_categories = random.randint(1, 3)
        categories = random.sample(CATEGORIES, k=num_categories)
        
        num_variants = random.randint(1, 4)
        variants = []
        
        for j in range(num_variants):
            color = colors[j % len(colors)]
            variant_id = ObjectId()
            sku = f"{manufacturer_name[:4].upper()}-{i:04d}-{color[:3].upper()}"
            
            base_price = round(random.uniform(100, 5000), 2)
            inventory_type = random.choice(["bulk", "serial"])
            
            variant = {
                "_id": variant_id,
                "sku": sku,
                "base_price": to_decimal(base_price),
                "attributes": {
                    "color": color
                },
                "inventory_type": inventory_type
            }
            
            if random.random() < 0.2:
                pass
            
            variants.append(variant)
            all_variants.append({
                "variant_id": variant_id,
                "product_id": None,
                "inventory_type": inventory_type
            })
        
        product = {
            "_id": ObjectId(),
            "name": f"{product_name} {manufacturer_name}",
            "description": description,
            "manufacturer": {
                "id": manufacturer_id,
                "name": manufacturer_name
            },
            "categories": categories,
            "base_attributes": {
                "warranty": f"{random.randint(12, 36)} miesięcy",
                "connection": random.choice(["Bluetooth 5.0", "USB-C", "WiFi", "Ethernet", "3.5mm"])
            },
            "avg_rating": to_decimal(round(random.uniform(3.5, 5.0), 1)),
            "review_count": random.randint(0, 500),
            "variants": variants
        }
        
        for variant_info in all_variants[-num_variants:]:
            variant_info["product_id"] = product["_id"]
        
        products.append(product)
    
    if products:
        insert_in_batches(db.products, products, batch_size=2000)
        print(f"Generated {len(products)} products with {sum(len(p['variants']) for p in products)} variants")
        return [p["_id"] for p in products], all_variants
    return [], []
