import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lesson-11", "generators")))
from db_connect import get_db
from pymongo import MongoClient
from bson import ObjectId
from queries_mongodb import QUERIES_MONGODB

import copy


def replace_params(obj, params):
    if isinstance(obj, dict):
        return {k: replace_params(v, params) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_params(item, params) for item in obj]
    elif isinstance(obj, str) and obj.startswith('{') and obj.endswith('}'):
        param_name = obj[1:-1]
        return params.get(param_name, obj)
    else:
        return obj

def fill_pipeline_params(pipeline, **params):
    pipeline = copy.deepcopy(pipeline)
    return replace_params(pipeline, params)

def run_query(query_id, db, collection_name, **params):
    desc, pipeline = QUERIES_MONGODB[query_id]
    pipeline = fill_pipeline_params(pipeline, **params)
    print(f"Zapytanie {query_id}: {desc}\n")
    results = list(db[collection_name].aggregate(pipeline))
    for doc in results:
        print(doc)
    # print(f"\nLiczba wyników: {len(results)}\n")
    return results

if __name__ == "__main__":
    db = get_db()
    print("Dostępne zapytania:")
    for qid, (desc, _) in QUERIES_MONGODB.items():
        print(f"{qid}: {desc}")
    try:
        qnum = int(input("\nPodaj numer zapytania do uruchomienia: "))
        default_collections = {
            1: 'orders', 2: 'orders', 3: 'orders', 4: 'reviews', 5: 'orders',
            6: 'user_favorites', 7: 'inventory_bulk', 8: 'inventory_bulk', 9: 'products', 10: 'products',
            11: 'orders', 12: 'manufacturers', 13: 'promotions', 14: 'carts', 15: 'products',
            16: 'orders', 17: 'orders', 18: 'products', 19: 'carts', 20: 'products',
            21: 'user_favorites', 22: 'inventory_bulk', 23: 'products', 24: 'orders', 25: 'products',
            26: 'products', 27: 'orders', 28: 'orders'
        }
        if qnum in default_collections:
            collection = default_collections[qnum]
        else:
            collection = input("Podaj nazwę kolekcji: ")
        params = {}
        if qnum == 20:
            params['search'] = input("Podaj frazę do wyszukania (name/description): ")
        if qnum == 21:
            params['product_id'] = input("Podaj _id produktu (ObjectId jako string): ")
        if qnum == 22:
            params['variant_id'] = input("Podaj variant_id (ObjectId jako string): ")
        if qnum == 23:
            params['attribute'] = input("Podaj nazwę atrybutu (np. color): ")
            params['value'] = input("Podaj wartość atrybutu (np. red): ")
        if qnum == 24:
            params['email'] = input("Podaj email użytkownika: ")
        if qnum == 25:
            params['product_id'] = input("Podaj _id produktu (ObjectId jako string): ")
        run_query(qnum, db, collection, **params)
    except Exception as e:
        print(f"Błąd: {e}")
