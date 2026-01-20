import random
from bson import ObjectId
from datetime import datetime, timedelta

def generate_inventory_serial():
    status_list = ["available", "reserved", "sold", "damaged", "returned"]
    history = []
    for _ in range(random.randint(1, 3)):
        history.append({
            "date": datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            "status": random.choice(status_list),
            "note": ""
        })
    return {
        "_id": ObjectId(),
        "serial_number": f"SN{random.randint(10000,99999)}",
        "status": random.choice(status_list),
        "variant_id": ObjectId(),
        "warehouse_id": ObjectId(),
        "history": history
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_inventory_serial())
