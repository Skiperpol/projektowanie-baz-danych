from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["projektowanie-mongodb"]

db.orders.create_index([("user_id", 1)])
db.orders.create_index([("order_date", 1)])
db.orders.create_index([("items.product_id", 1)])
db.orders.create_index([("items.variant_id", 1)])
db.orders.create_index([("payment_method", 1)])
db.orders.create_index([("shipping_address.city", 1)])
db.orders.create_index([("billing_address.city", 1)])

db.products.create_index([("variants._id", 1)])
db.products.create_index([("categories.id", 1)])
db.products.create_index([("manufacturer._id", 1)])
db.products.create_index([("variants.current_promotion.promo_id", 1)])
db.products.create_index([("name", 1)])
db.products.create_index([("description", 1)])

db.reviews.create_index([("product_id", 1)])

db.user_favorites.create_index([("product_id", 1)])
db.user_favorites.create_index([("user_id", 1)])

db.warehouses.create_index([("_id", 1)])

db.inventory_bulk.create_index([("variant_id", 1)])
db.inventory_bulk.create_index([("warehouse_id", 1)])

db.promotions.create_index([("_id", 1)])
db.promotions.create_index([("is_active", 1)])

db.carts.create_index([("user_id", 1)])
db.carts.create_index([("items.variant_id", 1)])
db.carts.create_index([("items.product_id", 1)])

db.users.create_index([("email", 1)])

print("Indeksy utworzone!")
