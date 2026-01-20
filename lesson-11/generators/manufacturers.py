import random
from bson import ObjectId

def generate_manufacturer():
    return {
        "_id": ObjectId(),
        "name": "ProducentY",
        "active": True,
        "description": "Opis producenta.",
        "website": "https://producenty.pl",
        "contact": {
            "email": "kontakt@producenty.pl",
            "phone": "987654321"
        },
        "address": {
            "city": "Miasto",
            "street": "Ulica 5",
            "zip_code": "00-000"
        }
    }

if __name__ == "__main__":
    from pprint import pprint
    pprint(generate_manufacturer())
