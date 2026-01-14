import random
from bson import ObjectId

def generate_inventory_bulk():
    return {
        "_id": ObjectId(),
        "variant_id": ObjectId(),
        "warehouse_id": ObjectId(),
        "quantity_on_hand": random.randint(0, 100),
        "quantity_reserved": random.randint(0, 50)
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_inventory_bulk())
