from bson import ObjectId
from faker import Faker
from config import get_db, insert_in_batches
from datetime import datetime, timedelta
from pymongo.errors import PyMongoError
import random

fake = Faker('pl_PL')


def generate_serial_number(prefix="SN"):
    """Generate a unique serial number"""
    return f"{prefix}-{fake.bothify(text='??-####-####-####').upper()}"


def generate_inventory_serial(count, variants_info, warehouse_ids):
    """Generate inventory_serial collection"""
    db = get_db()
    inventory_items = []
    
    serial_variants = [v for v in variants_info if v.get("inventory_type") == "serial"]
    
    if not serial_variants:
        print("No serial inventory variants found")
        return []
    
    if not warehouse_ids:
        print("No warehouses found. Please generate warehouses first.")
        return []
    
    statuses = ['available', 'reserved', 'sold', 'damaged', 'returned']
    status_weights = [0.6, 0.15, 0.15, 0.05, 0.05]
    
    for i in range(count):
        variant_info = random.choice(serial_variants)
        warehouse_id = random.choice(warehouse_ids)
        status = random.choices(statuses, weights=status_weights)[0]
        
        history = []
        num_history_events = random.randint(1, 3)
        
        start_date = datetime.now() - timedelta(days=random.randint(1, 365))
        
        for j in range(num_history_events):
            event_date = start_date + timedelta(days=j * random.randint(1, 30))
            event_status = statuses[j] if j < len(statuses) else random.choice(statuses)
            
            history_event = {
                "date": event_date,
                "status": event_status
            }
            
            if random.random() < 0.3:
                history_event["note"] = fake.sentence()
            
            history.append(history_event)
        
        if not any(h["status"] == status for h in history):
            history.append({
                "date": datetime.now(),
                "status": status
            })
        
        inventory_item = {
            "_id": ObjectId(),
            "serial_number": generate_serial_number(),
            "variant_id": variant_info["variant_id"],
            "warehouse_id": warehouse_id,
            "status": status,
            "history": history
        }
        inventory_items.append(inventory_item)
    
    if inventory_items:
        try:
            insert_in_batches(db.inventory_serial, inventory_items, batch_size=2000)
            print(f"Generated {len(inventory_items)} serial inventory items")
            return [item["_id"] for item in inventory_items]
        except PyMongoError as e:
            print("Error inserting inventory_serial documents:", e)
            if inventory_items:
                print("Sample inventory_serial document that failed validation:")
                print(inventory_items[0])
            return []
    return []
