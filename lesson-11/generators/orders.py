import random
from bson import ObjectId, Decimal128
from datetime import datetime

def generate_order():
    return {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "order_date": datetime.utcnow(),
        "payment_method": "card",
        "status": random.choice(["new", "payment_pending", "processing", "shipped", "completed", "cancelled"]),
        "total_amount": Decimal128(str(round(random.uniform(50, 500), 2))),
        "items": [
            {
                "name": "ProduktX",
                "product_id": ObjectId(),
                "quantity": random.randint(1, 5),
                "unit_price": Decimal128(str(round(random.uniform(10, 100), 2))),
                "variant_sku": "SKU" + str(random.randint(1000, 9999))
            }
        ],
        "billing_address": {
            "street": "Ulica 1",
            "city": "Miasto",
            "postal_code": "00-000",
            "country": "PL"
        },
        "shipping_address": {
            "street": "Ulica 2",
            "city": "Miasto",
            "postal_code": "00-000",
            "country": "PL"
        },
        "delivery_method": {
            "name": "Kurier",
            "cost": Decimal128(str(round(random.uniform(10, 30), 2)))
        }
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_order())
