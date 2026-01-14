from bson import ObjectId
from config import get_db, insert_in_batches
from pymongo.errors import PyMongoError
import random


def generate_inventory_bulk(count, variants_info, warehouse_ids):
    """Generate inventory_bulk collection"""
    db = get_db()
    inventory_items = []
    
    bulk_variants = [v for v in variants_info if v.get("inventory_type") == "bulk"]
    
    if not bulk_variants:
        print("No bulk inventory variants found")
        return []
    
    if not warehouse_ids:
        print("No warehouses found. Please generate warehouses first.")
        return []
    
    for variant_info in bulk_variants:
        num_warehouses = random.randint(1, min(3, len(warehouse_ids)))
        selected_warehouses = random.sample(warehouse_ids, k=num_warehouses)
        
        for warehouse_id in selected_warehouses:
            quantity_on_hand = random.randint(0, 500)
            quantity_reserved = random.randint(0, min(50, quantity_on_hand))
            
            inventory_item = {
                "_id": ObjectId(),
                "variant_id": variant_info["variant_id"],
                "warehouse_id": warehouse_id,
                "quantity_on_hand": quantity_on_hand,
                "quantity_reserved": quantity_reserved
            }
            inventory_items.append(inventory_item)
    
    while len(inventory_items) < count and bulk_variants:
        variant_info = random.choice(bulk_variants)
        warehouse_id = random.choice(warehouse_ids)
        
        quantity_on_hand = random.randint(0, 500)
        quantity_reserved = random.randint(0, min(50, quantity_on_hand))
        
        inventory_item = {
            "_id": ObjectId(),
            "variant_id": variant_info["variant_id"],
            "warehouse_id": warehouse_id,
            "quantity_on_hand": quantity_on_hand,
            "quantity_reserved": quantity_reserved
        }
        inventory_items.append(inventory_item)
    
    if inventory_items:
        try:
            insert_in_batches(db.inventory_bulk, inventory_items, batch_size=2000)
            print(f"Generated {len(inventory_items)} bulk inventory items")
            return [item["_id"] for item in inventory_items]
        except PyMongoError as e:
            print("Error inserting inventory_bulk documents:", e)
            if inventory_items:
                print("Sample inventory_bulk document that failed validation:")
                print(inventory_items[0])
            return []
    return []
