QUERIES_MONGODB = {
    1: ("Średnia Wartość Zamówienia (AOV) w Ostatnim Miesiącu", [
        {
            "$match": {
                "$expr": {
                    "$and": [
                        {
                            "$gte": [
                                "$order_date",
                                {
                                    "$dateTrunc": {
                                        "date": {
                                            "$dateSubtract": {
                                                "startDate": "$$NOW",
                                                "unit": "month",
                                                "amount": 1
                                            }
                                        },
                                        "unit": "month"
                                    }
                                }
                            ]
                        },
                        {
                            "$lt": [
                                "$order_date",
                                {
                                    "$dateTrunc": {
                                        "date": "$$NOW",
                                        "unit": "month"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$user_id", "total_price": {
                    "$sum": "$total_amount"
                }
            }
        },
        {
            "$group": {
                "_id": None, "avg_order_value": {
                    "$avg": "$total_price"
                }
                }
        },
        {
            "$project": {
                "_id": 0,
                "avg_order_value": 1
            }
        }
    ]
    ),

    2: ("Średnia wartość zamówienia per użytkownik", [
        {
            "$group": {
                "_id": "$user_id", 
                "avg_order_value": {
                    "$avg": "$total_amount"
                }
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {"$unwind": "$user"},
        {
            "$project": {
                "user_id": "$_id",
                "first_name": "$user.first_name",
                "last_name": "$user.last_name",
                "avg_order_value": 1,
                "_id": 0
            }
        },
        {"$sort": {"avg_order_value": -1}}
    ]),

    3: ("Top 10 Najlepiej Sprzedających Się Produktów (wg. Ilości Sprzedanych Jednostek) w Ostatnim Kwartale", [
        {
            "$match": {
                "$expr": {
                    "$gte": [
                        "$order_date",
                        {
                            "$dateSubtract": {
                                "startDate": "$$NOW",
                                "unit": "month",
                                "amount": 3
                            }
                        }
                    ]
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": "$items.product_id",
                "total_units_sold": {"$sum": "$items.quantity"}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {
            "$unwind": "$product"
        },
        {
            "$project": {
                "product_name": "$product.name",
                "total_units_sold": 1
            }
        },
        {
            "$sort": {"total_units_sold": -1}
        },
        {
            "$limit": 10
        }
    ]),

    4: ("Top 5 produktów z najwięcej recenzjami", [
        {
            "$group": {
                "_id": "$product_id",
                "reviews_count": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {
            "$unwind": "$product"
        },
        {
            "$project": {
                "product_name": "$product.name",
                "reviews_count": 1
            }
        },
        {
            "$sort": {"reviews_count": -1}
        },
        {
            "$limit": 5
        }
    ]),

    5: ("Całkowity Przychód Pogrupowany Miesięcznie za Ostatni Rok", [
        {
            "$match": {
                "$expr": {
                    "$gte": [
                        "$order_date",
                        {
                            "$dateSubtract": {
                                "startDate": "$$NOW",
                                "unit": "year",
                                "amount": 1
                            }
                        }
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m",
                        "date": "$order_date"
                    }
                },
                "monthly_revenue": {"$sum": "$total_amount"}
            }
        },
        {
            "$sort": {"_id": -1}
        }
    ]),

    6: ("Produkty najczęściej dodawane do ulubionych", [
        {
            "$group": {"_id": "$product_id", "favorites_count": {"$sum": 1}}
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {
            "$project": {"product_name": "$product.name", "favorites_count": 1}
        },
        {"$sort": {"favorites_count": -1}},
        {"$limit": 10}
    ]),

    7: ("Dostępny Stan Magazynowy Wariantów Produktu Pogrupowany po Magazynach", [
        {
            "$group": {
                "_id": {"variant_id": "$variant_id", "warehouse_id": "$warehouse_id"},
                "stock_count": {"$sum": "$quantity_on_hand"}
            }
        },
        {
            "$lookup": {
                "from": "warehouses",
                "localField": "_id.warehouse_id",
                "foreignField": "_id",
                "as": "warehouse"
            }
        },
        {"$unwind": "$warehouse"},
        {
            "$lookup": {
                "from": "products",
                "localField": "_id.variant_id",
                "foreignField": "variants._id",
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {
            "$project": {
                "product_name": "$product.name",
                "warehouse_name": "$warehouse.name",
                "stock_count": 1
            }
        },
        {"$sort": {"product_name": 1, "warehouse_name": 1}}
    ]),

    # if u know u know
    8: ("Stan magazynowy per wariant produktu", [
        {
            "$group": {
                "_id": "$variant_id",
                "stock_count": {"$sum": "$quantity_on_hand"}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "let": {"variant_id": "$_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$in": ["$$variant_id", "$variants._id"]}}},
                    {"$project": {"name": 1}}
                ],
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {
            "$project": {
                "variant_id": "$_id",
                "product_name": "$product.name",
                "stock_count": 1
            }
        },
        {"$sort": {"stock_count": -1}}
    ]),

    # if u still know u know
    9: ("Najpopularniejsze Kategorie (wg. Całkowitego Przychodu)", [
        {"$unwind": "$categories"},
        {
            "$group": {
                "_id": "$categories.id",
                "total_category_revenue": {"$sum": "$base_price"}
            }
        },
        {
            "$lookup": {
                "from": "products",
                "let": {"cat_id": "$_id"},
                "pipeline": [
                    {"$match": {"$expr": {"$in": ["$$cat_id", "$categories.id"]}}},
                    {"$project": {"categories.name": 1}}
                ],
                "as": "category"
            }
        },
        {"$unwind": "$category"},
        {
            "$project": {"category_name": "$category.categories.name", "total_category_revenue": 1}
        },
        {"$sort": {"total_category_revenue": -1}},
        {"$limit": 10}
    ]),

    #if u definitely know u know
    10: ("Liczba produktów per kategoria", [
        {"$unwind": "$categories"},
        {
            "$group": {"_id": "$categories.id", "products_count": {"$sum": 1}}
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "categories.id",
                "as": "category"
            }
        },
        {"$unwind": "$category"},
        {
            "$project": {"category_name": "$category.categories.name", "products_count": 1}
        },
        {"$sort": {"products_count": -1}}
    ]),

    11: ("Liczba zamówień per metoda płatności", [
        {
            "$group": {"_id": "$payment_method", "orders_count": {"$sum": 1}, "total_value": {"$sum": "$total_amount"}}
        },
        {"$sort": {"total_value": -1}}
    ]),

    # do poprawy
    12: ("Średnia ocena per producent", [
    {
        "$lookup": {
            "from": "products",
            "localField": "_id", 
            "foreignField": "manufacturer._id", 
            "as": "products"
        }
    },
    { "$unwind": "$products" },
    {
        "$lookup": {
            "from": "reviews",
            "localField": "products._id",
            "foreignField": "product_id",
            "as": "product_reviews"
        }
    },
    { "$unwind": "$product_reviews" },
    {
        "$group": {
            "_id": "$_id",
            "manufacturer_name": { "$first": "$name" },
            "avg_rating": { "$avg": "$product_reviews.rating" }
        }
    },
    { "$sort": { "avg_rating": -1 } }
    ]),

    # do poprawy
    13: ("Aktywne promocje i objęta nimi liczba wariantów", [
        {
            "$match": {"is_active": True}
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "variants.current_promotion.promo_id",
                "as": "products"
            }
        },
        {"$unwind": "$products"},
        {
            "$project": {"promotion_name": "$name", "active_discount_items": {"$size": "$products.variants"}}
        },
        {"$sort": {"active_discount_items": -1}}
    ]),

    
    14: ("Najczęściej wybierane warianty w koszykach", [
        {"$unwind": "$items"},
        {
            "$group": {"_id": "$items.variant_id", "total_quantity": {"$sum": "$items.quantity"}}
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "variants._id",
                "as": "variant"
            }
        },
        {"$unwind": "$variant"},
        {
            "$project": {"variant_sku": "$variant.variants.sku", "product_name": "$variant.name", "total_quantity": 1}
        },
        {"$sort": {"total_quantity": -1}},
        {"$limit": 10}
    ]),

    15: ("Produkty z Największą Różnicą Między Ceną Podstawową a Ceną Wariantu", [
        {"$unwind": "$variants"},
        {
            "$project": {
                "product_name": "$name",
                "sku": "$variants.sku",
                "base_price": "$variants.base_price",
                "final_variant_price": {"$add": ["$variants.base_price", 0]},
                "price_difference": {"$subtract": ["$variants.base_price", 0]}
            }
        },
        {"$sort": {"price_difference": -1}},
        {"$limit": 10}
    ]),

    16: ("Konwersja zamówień wg statusu", [
        {
            "$group": {"_id": "$status", "orders_count": {"$sum": 1}}
        },
        {
            "$group": {
                "_id": None,
                "total_orders": {"$sum": "$orders_count"},
                "statuses": {"$push": {"status": "$_id", "orders_count": "$orders_count"}}
            }
        }
    ]),

    17: ("Top klienci wg wydatków", [
        {
            "$group": {"_id": "$user_id", "total_spent": {"$sum": "$total_amount"}}
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {"$unwind": "$user"},
        {
            "$project": {"user_id": "$_id", "first_name": "$user.first_name", "last_name": "$user.last_name", "total_spent": 1}
        },
        {"$sort": {"total_spent": -1}},
        {"$limit": 10}
    ]),

    18: ("Produkty z wariantami objętymi promocją, z końcową ceną", [
        {"$unwind": "$variants"},
        {
            "$match": {"variants.current_promotion": {"$exists": True}}
        },
        {
            "$project": {
                "product_name": "$name",
                "sku": "$variants.sku",
                "final_price": "$variants.current_promotion.final_price",
                "promo_id": "$variants.current_promotion.promo_id"
            }
        }
    ]),

    19: ("Użytkownicy, Którzy Dodali Produkt do Koszyka, Ale Nie Złożyli Zamówienia", [
        {
            "$lookup": {
                "from": "orders",
                "localField": "user_id",
                "foreignField": "user_id",
                "as": "orders"
            }
        },
        {"$match": {"orders": {"$size": 0}}},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {
            "$project": {"user_id": "$user_id", "product_in_cart": "$product.name"}
        }
    ]),

    20: ("Wyszukiwanie produktów po nazwie lub opisie (parametryzowane)", [
        {
            "$match": {"$or": [
                {"name": {"$regex": "{search}", "$options": "i"}},
                {"description": {"$regex": "{search}", "$options": "i"}}
            ]}
        },
        {
            "$project": {"_id": 1, "name": 1, "description": 1, "base_price": 1}
        }
    ]),

    21: ("Użytkownicy, Którzy Zapisali Konkretny Produkt jako Ulubiony (ObjectId)", [
        {"$match": {"$expr": {"$eq": ["$product_id", {"$toObjectId": "{product_id}"}]}}},
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$project": {"email": "$user.email", "first_name": "$user.first_name", "last_name": "$user.last_name"}}
    ]),

    #na pewno dziala dla bulk 
    22: ("Magazyny, Które Posiadają Zapasy Konkretnego Wariantu (np. variant_id=ObjectId)", [
        {"$match": {"$expr": {"$eq": ["$variant_id", {"$toObjectId": "{variant_id}"}]}}},
        {"$lookup": {
            "from": "warehouses",
            "localField": "warehouse_id",
            "foreignField": "_id",
            "as": "warehouse"
        }},
        {"$unwind": "$warehouse"},
        {"$group": {"_id": "$warehouse.name", "stock_count": {"$sum": "$quantity_on_hand"}}},
        {"$match": {"stock_count": {"$gt": 0}}}
    ]),

    23: ("Warianty, Które Wymagają Uzyskania Konkretnej Opcji (parametryzowane)", [
        {"$unwind": "$variants"},
        {"$match": {"$expr": {"$eq": [
            {"$getField": {"field": "{attribute}", "input": "$variants.attributes"}},
            "{value}"
        ]}}},
        {"$project": {"sku": "$variants.sku", "product_name": "$name"}}
    ]),

    24: ("Wszystkie zamówienia użytkownika po emailu", [
        {"$lookup": {
            "from": "users",
            "localField": "user_id",
            "foreignField": "_id",
            "as": "user"
        }},
        {"$unwind": "$user"},
        {"$match": {"user.email": "{email}"}},
        {"$project": {"order_id": "$_id", "order_date": 1, "status": 1}}
    ]),

    25: ("Wszystkie Warianty i Ich Ceny dla Konkretnego Produktu (np. _id=ObjectId)", [
        {"$match": {"$expr": {"$eq": ["$_id", {"$toObjectId": "{product_id}"}]}}},
        {"$unwind": "$variants"},
        {"$project": {"sku": "$variants.sku", "color": "$variants.attributes.color", "base_price": "$variants.base_price", "current_price": "$variants.base_price"}}
    ]),

   
    # do poprawy
    26: ("Porównanie Średniej Oceny dla Promowanych i Niepromowanych Produktów", [
        {"$unwind": "$variants"},
        {"$lookup": {
            "from": "reviews",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "reviews"
        }},
        {"$addFields": {"promotion_status": {"$cond": [{"$ifNull": ["$variants.current_promotion", False]}, "Promowany", "Niepromowany"]}}},
        {"$unwind": "$reviews"},
        {"$group": {"_id": "$promotion_status", "average_rating": {"$avg": "$reviews.rating"}}}
    ]),

    27: ("Top 5 Miast Generujących Największy Przychód (Wg. Adresu Wysyłki)", [
        {"$group": {"_id": "$shipping_address.city", "city_revenue": {"$sum": "$total_amount"}}},
        {"$sort": {"city_revenue": -1}},
        {"$limit": 5}
    ]),

    # do poprawy
    28: ("Porównanie Wolumenu Sprzedaży Produktów Promowanych vs. Niepromowanych (w Ostatnich 30 Dniach)", [
        {"$match": {"order_date": {"$gte": {"$dateSubtract": {"startDate": "$$NOW", "unit": "day", "amount": 30}}}}},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {"$unwind": "$product"},
        {"$unwind": "$product.variants"},
        {"$match": {"$expr": {"$eq": ["$items.variant_id", "$product.variants._id"]}}},
        {"$addFields": {"promotion_status": {"$cond": [{"$ifNull": ["$product.variants.current_promotion", False]}, "Promowany", "Niepromowany"]}}},
        {"$group": {"_id": "$promotion_status", "total_units_sold": {"$sum": "$items.quantity"}}}
    ]),

    29: ("Wskaźnik Lojalności (Repeat Purchase Rate) Użytkowników z Podziałem na Miasto Adresu Rozliczeniowego", [
        {"$group": {"_id": {"user_id": "$user_id", "city": "$billing_address.city"}, "orders_count": {"$sum": 1}}},
        {"$group": {"_id": "$_id.city", "repeat_customers": {"$sum": {"$cond": [{"$gt": ["$orders_count", 1]}, 1, 0]}}, "total_customers": {"$sum": 1}}},
        {"$project": {"repeat_purchase_rate": {"$cond": [ {"$eq": ["$total_customers", 0]}, 0, {"$round": [{"$multiply": [{"$divide": ["$repeat_customers", "$total_customers"]}, 100]}, 2]}]}, "repeat_customers": 1, "total_customers": 1}},
        {"$sort": {"repeat_purchase_rate": -1}}
    ])
    
    }
