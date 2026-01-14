#!/usr/bin/env python3
"""
Main script to generate MongoDB data for e-commerce database.
Generates data in the correct order to maintain referential integrity.
"""

from config import get_db, load_counts
from generators.manufacturers import generate_manufacturers
from generators.warehouses import generate_warehouses
from generators.users import generate_users
from generators.products import generate_products, CATEGORIES
from generators.promotions import generate_promotions
from generators.inventory_bulk import generate_inventory_bulk
from generators.inventory_serial import generate_inventory_serial
from generators.carts import generate_carts
from generators.orders import generate_orders
from generators.reviews import generate_reviews
from generators.user_favorites import generate_user_favorites

def clear_database():
    """Clear all collections"""
    db = get_db()
    collections = [
        'manufacturers', 'warehouses', 'users', 'products',
        'promotions', 'inventory_bulk', 'inventory_serial',
        'carts', 'orders', 'reviews', 'user_favorites'
    ]
    
    response = input("Do you want to clear existing data? (yes/no): ")
    if response.lower() == 'yes':
        for collection in collections:
            db[collection].delete_many({})
        print("Database cleared.")
    else:
        print("Keeping existing data.")

def main():
    """Main function to generate all data"""
    print("=" * 60)
    print("MongoDB Data Generator for E-commerce Database")
    print("=" * 60)
    
    # Load counts
    counts = load_counts()
    print(f"\nLoaded configuration:")
    for key, value in counts.items():
        print(f"  {key}: {value}")
    
    # Ask about clearing database
    clear_database()
    
    print("\n" + "=" * 60)
    print("Starting data generation...")
    print("=" * 60 + "\n")
    
    # Step 1: Generate basic entities (no dependencies)
    print("Step 1: Generating manufacturers...")
    manufacturer_ids = generate_manufacturers(counts['manufacturers'])
    
    print("\nStep 2: Generating warehouses...")
    warehouse_ids = generate_warehouses(counts['warehouses'])
    
    print("\nStep 3: Generating users...")
    user_ids = generate_users(counts['users'])
    
    # Step 2: Generate products (depends on manufacturers)
    print("\nStep 4: Generating products...")
    product_ids, variants_info = generate_products(counts['products'], manufacturer_ids)
    
    # Step 3: Generate promotions (depends on products)
    print("\nStep 5: Generating promotions...")
    category_ids = [cat["id"] for cat in CATEGORIES]
    promotion_ids = generate_promotions(counts['promotions'], product_ids, category_ids)
    
    # Step 4: Generate inventory (depends on products and warehouses)
    print("\nStep 6: Generating inventory (bulk)...")
    inventory_bulk_ids = generate_inventory_bulk(
        counts['inventory_bulk'],
        variants_info,
        warehouse_ids
    )
    
    print("\nStep 7: Generating inventory (serial)...")
    inventory_serial_ids = generate_inventory_serial(
        counts['inventory_serial'],
        variants_info,
        warehouse_ids
    )
    
    # Step 5: Generate user-related data (depends on users and products)
    print("\nStep 8: Generating carts...")
    cart_ids = generate_carts(counts['carts'], user_ids, product_ids)
    
    print("\nStep 9: Generating orders...")
    order_ids = generate_orders(counts['orders'], user_ids, product_ids)
    
    print("\nStep 10: Generating reviews...")
    review_ids = generate_reviews(counts['reviews'], user_ids, product_ids)
    
    print("\nStep 11: Generating user favorites...")
    favorite_ids = generate_user_favorites(counts['user_favorites'], user_ids, product_ids)
    
    # Summary
    print("\n" + "=" * 60)
    print("Data generation completed!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Manufacturers: {len(manufacturer_ids)}")
    print(f"  Warehouses: {len(warehouse_ids)}")
    print(f"  Users: {len(user_ids)}")
    print(f"  Products: {len(product_ids)}")
    print(f"  Promotions: {len(promotion_ids)}")
    print(f"  Inventory (bulk): {len(inventory_bulk_ids)}")
    print(f"  Inventory (serial): {len(inventory_serial_ids)}")
    print(f"  Carts: {len(cart_ids)}")
    print(f"  Orders: {len(order_ids)}")
    print(f"  Reviews: {len(review_ids)}")
    print(f"  User Favorites: {len(favorite_ids)}")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
