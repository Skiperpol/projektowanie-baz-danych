# Przykładowy generator uruchamiający generowanie danych dla wszystkich kolekcji
import json
import os
from db_connect import get_db
from carts import generate_cart
from products import generate_product
from orders import generate_order
from users import generate_user
from warehouses import generate_warehouse
from reviews import generate_review
from promotions import generate_promotion
from inventory_bulk import generate_inventory_bulk
from manufacturers import generate_manufacturer

# Ścieżka do row_counts.json
ROW_COUNTS_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..", "..", "lesson-12", "mongodb-generator", "config", "row_counts.json"
    )
)

def load_row_counts():
    with open(ROW_COUNTS_PATH, encoding="utf-8") as f:
        return json.load(f)

COLLECTIONS = {
    "warehouses": generate_warehouse,
    "manufacturers": generate_manufacturer,
    "users": generate_user,
    "products": generate_product,
    "inventory_bulk": generate_inventory_bulk,
    "carts": generate_cart,
    "orders": generate_order,
    "reviews": generate_review,
    "promotions": generate_promotion
}

def insert_sample_data(db, row_counts):
    print("=" * 60)
    print("MongoDB Data Generator for lesson-11")
    print("=" * 60)
    print(f"\nPołączono z bazą: {db.name}")
    print("\nCheckpoint: Start generowania danych...")
    for name, gen_func in COLLECTIONS.items():
        n = row_counts.get(name, 0)
        print(f"Checkpoint: Generowanie kolekcji {name} ({n} dokumentów)...")
        docs = [gen_func() for _ in range(n)]
        if docs:
            db[name].insert_many(docs)
            print(f"Checkpoint: Wstawiono {n} dokumentów do kolekcji {name}")
        else:
            print(f"Checkpoint: Pominięto kolekcję {name} (0 dokumentów)")
    print("\nCheckpoint: Wszystkie dane wygenerowane!")
    print("=" * 60)

if __name__ == "__main__":
    db = get_db()
    row_counts = load_row_counts()
    insert_sample_data(db, row_counts)
