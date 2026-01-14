import random
from bson import ObjectId, Decimal128

def generate_product():
    return {
        "_id": ObjectId(),
        "name": "Produkt " + str(random.randint(1, 100)),
        "description": "Opis produktu.",
        "avg_rating": Decimal128(str(round(random.uniform(1, 5), 2))),
        "review_count": random.randint(0, 100),
        "base_attributes": {
            "connection": "USB",
            "warranty": "24m"
        },
        "manufacturer": {
            "id": ObjectId(),
            "name": "ProducentX"
        },
        "categories": [
            {"id": ObjectId(), "name": "KategoriaA"}
        ],
        "variants": [
            {
                "_id": ObjectId(),
                "sku": "SKU" + str(random.randint(1000, 9999)),
                "inventory_type": "bulk",
                "base_price": Decimal128(str(round(random.uniform(10, 100), 2))),
                "attributes": {"color": "red"},
                "current_promotion": {
                    "final_price": Decimal128(str(round(random.uniform(5, 90), 2))),
                    "promo_id": ObjectId()
                }
            }
        ]
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_product())
