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
                "_id": None,
                "avg_order_value": {"$avg": "$total_amount"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "avg_order_value": {"$round": ["$avg_order_value", 2]}
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
                "avg_order_value": {"$round": ["$avg_order_value", 2]},
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
                "let": { "pid": "$_id" },
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$_id", "$$pid"] } } },
                    { "$project": { "name": 1, "_id": 0 } }
                ],
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
                "let": { "pid": "$_id" },
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$_id", "$$pid"] } } },
                    { "$project": { "name": 1, "_id": 0 } }
                ],
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
                    "$and": [
                        {"$gte": [
                            "$order_date",
                            {"$dateTrunc": {
                                "date": {"$dateFromString": {"dateString": "2025-01-01T00:00:00Z"}},
                                "unit": "year"
                            }}
                        ]},
                        {"$lt": [
                            "$order_date",
                            {"$dateAdd": {
                                "startDate": {"$dateTrunc": {
                                    "date": {"$dateFromString": {"dateString": "2025-01-01T00:00:00Z"}},
                                    "unit": "year"
                                }},
                                "unit": "year",
                                "amount": 1
                            }}
                        ]}
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
            "$sort": {"_id": 1}
        }
    ]),

    6: ("Produkty najczęściej dodawane do ulubionych", [
        {
            "$group": {"_id": "$product_id", "favorites_count": {"$sum": 1}}
        },
        {
            "$lookup": {
                "from": "products",
                "let": { "pid": "$_id" },
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$_id", "$$pid"] } } },
                    { "$project": { "name": 1, "_id": 0 } }
                ],
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

    # działa dla małych ilości danych
    7: ("Dostępny Stan Magazynowy Wariantów Produktu Pogrupowany po Magazynach", [
        {
            "$project": {
                "variant_id": 1,
                "warehouse_id": 1,
                "quantity": "$quantity_on_hand"
            }
        },
        {
            "$unionWith": {
                "coll": "inventory_serial",
                "pipeline": [
                    { "$match": { "status": "available" } },
                    { "$project": { "variant_id": 1, "warehouse_id": 1, "quantity": { "$literal": 1 } } }
                ]
            }
        },
        {
            "$group": {
                "_id": { "v_id": "$variant_id", "w_id": "$warehouse_id" },
                "stock_count": { "$sum": "$quantity" }
            }
        },
        {
            "$lookup": {
                "from": "warehouses",
                "localField": "_id.w_id",
                "foreignField": "_id",
                "as": "warehouse"
            }
        },
        { "$unwind": "$warehouse" },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id.v_id",
                "foreignField": "variants._id",
                "as": "product"
            }
        },
        { "$unwind": "$product" },
        {
            "$project": {
                "product_name": "$product.name",
                "warehouse_name": "$warehouse.name",
                "stock_count": 1,
                "_id": 0
            }
        },
        { "$sort": { "product_name": 1, "warehouse_name": 1 } }
    ]),

    # działa dla małych ilości danych
    8: ("Stan magazynowy per wariant produktu", [
        { "$project": { "variant_id": 1, "qty": "$quantity_on_hand" } },
        {
            "$unionWith": {
                "coll": "inventory_serial",
                "pipeline": [
                    { "$match": { "status": "available" } },
                    { "$project": { "variant_id": 1, "qty": { "$literal": 1 } } }
                ]
            }
        },
        {
            "$group": {
                "_id": "$variant_id",
                "stock_count": { "$sum": "$qty" }
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "variants._id",
                "as": "product_info"
            }
        },
        { "$unwind": "$product_info" },
        {
            "$project": {
                "variant_id": "$_id",
                "product_name": "$product_info.name",
                "stock_count": 1,
                "_id": 0
            }
        },
        { "$sort": { "stock_count": -1 } }
    ]),

    9: ("Najpopularniejsze Kategorie (wg. Całkowitego Przychodu)", [
        {"$unwind": "$variants"},
        {"$unwind": "$categories"},
        {
            "$group": {
                "_id": "$categories.id",
                "category_name": {"$first": "$categories.name"},
                "total_category_revenue": {"$sum": "$variants.base_price"}
            }
        },
        {
            "$project": {"category_name": 1, "total_category_revenue": 1, "_id": 0}
        },
        {"$sort": {"total_category_revenue": -1}},
        {"$limit": 10}
    ]),

    10: ("Liczba produktów per kategoria", [
        {"$unwind": "$categories"},
        {
            "$group": {
                "_id": "$categories.id",
                "category_name": {"$first": "$categories.name"},
                "products_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "category_name": 1,
                "products_count": 1,
                "_id": 0
            }
        },
        {"$sort": {"products_count": -1}}
    ]),

    11: ("Liczba zamówień per metoda płatności", [
        {
            "$group": {"_id": "$payment_method", "orders_count": {"$sum": 1}, "total_value": {"$sum": "$total_amount"}}
        },
        {"$sort": {"total_value": -1}}
    ]),

    12: ("Średnia ocena per producent (ważona)", [
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "manufacturer.id",
                "as": "product_stats"
            }
        },
        { "$unwind": "$product_stats" },
        {
            "$group": {
                "_id": "$_id",
                "manufacturer_name": { "$first": "$name" },
                "total_weighted_rating": {
                    "$sum": { "$multiply": ["$product_stats.avg_rating", "$product_stats.review_count"] }
                },
                "total_reviews": { "$sum": "$product_stats.review_count" }
            }
        },
        {
            "$project": {
                "manufacturer_name": 1,
                "review_count": "$total_reviews",
                "avg_rating": {
                    "$cond": [
                        { "$eq": ["$total_reviews", 0] },
                        0,
                        { "$round": [ { "$divide": ["$total_weighted_rating", "$total_reviews"] }, 2 ] }
                    ]
                }
            }
        },
        { "$sort": { "avg_rating": -1 } }
    ]),

    13: ("Aktywne promocje i objęta nimi liczba wariantów", [
        { "$match": { "is_active": True } },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "variants.current_promotion.promo_id",
                "as": "matched_products"
            }
        },
        {
            "$project": {
                "promotion_name": "$name",
                "active_discount_items": {
                    "$reduce": {
                        "input": "$matched_products",
                        "initialValue": 0,
                        "in": {
                            "$add": [
                                "$$value",
                                {
                                    "$size": {
                                        "$filter": {
                                            "input": "$$this.variants",
                                            "as": "variant",
                                            "cond": { "$eq": ["$$variant.current_promotion.promo_id", "$_id"] }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        { "$sort": { "active_discount_items": -1 } }
    ]),

    
    14: ("Najczęściej wybierane warianty w koszykach", [
        { "$unwind": "$items" },
        {
            "$group": {
                "_id": "$items.variant_id",
                "total_quantity": { "$sum": "$items.quantity" }
            }
        },
        { "$sort": { "total_quantity": -1 } },
        { "$limit": 10 },
        {
            "$lookup": {
                "from": "products",
                "localField": "_id",
                "foreignField": "variants._id",
                "as": "product_doc"
            }
        },
        { "$unwind": "$product_doc" },
        {
            "$project": {
                "_id": 0,
                "total_quantity": 1,
                "product_name": "$product_doc.name",
                "variant_data": {
                    "$arrayElemAt": [
                        {
                            "$filter": {
                                "input": "$product_doc.variants",
                                "as": "v",
                                "cond": { "$eq": ["$$v._id", "$_id"] }
                            }
                        },
                        0
                    ]
                }
            }
        },
        {
            "$project": {
                "product_name": 1,
                "total_quantity": 1,
                "sku": "$variant_data.sku",
                "color": "$variant_data.attributes.color",
                "base_price": "$variant_data.base_price"
            }
        }
    ]),

    15: ("Produkty z Największą Różnicą Między Ceną Podstawową a Ceną Promocyjną", [
        { "$unwind": "$variants" },
        {
            "$project": {
                "product_name": "$name",
                "sku": "$variants.sku",
                "base_price": "$variants.base_price",
                "final_price": { "$ifNull": ["$variants.current_promotion.final_price", "$variants.base_price"] },
                "price_difference": {
                    "$subtract": [
                        "$variants.base_price",
                        { "$ifNull": ["$variants.current_promotion.final_price", "$variants.base_price"] }
                    ]
                }
            }
        },
        { "$sort": { "price_difference": -1 } },
        { "$limit": 10 }
    ]),

    16: ("Konwersja zamówień wg statusu", [
        { "$group": { "_id": "$status", "count": { "$sum": 1 } } },
        { "$group": {
            "_id": None,
            "total_orders": { "$sum": "$count" },
            "status_data": { "$push": { "status": "$_id", "count": "$count" } }
        } },
        { "$unwind": "$status_data" },
        { "$project": {
            "_id": 0,
            "status": "$status_data.status",
            "orders_count": "$status_data.count",
            "total_orders": 1,
            "conversion_rate": {
                "$concat": [
                    { "$toString": { "$round": [ { "$multiply": [ { "$divide": [ "$status_data.count", "$total_orders" ] }, 100 ] }, 2 ] } },
                    "%"
                ]
            }
        } },
        { "$sort": { "orders_count": -1 } }
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
            "$project": {"_id": 0, "user_id": "$_id", "first_name": "$user.first_name", "last_name": "$user.last_name", "total_spent": 1}
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
                "_id": 0,
                "product_name": "$name",
                "sku": "$variants.sku",
                "final_price": "$variants.current_promotion.final_price",
                "promo_id": "$variants.current_promotion.promo_id"
            }
        }
    ]),

    # działa dla małych ilości danych
    19: ("Użytkownicy, Którzy Dodali Produkt do Koszyka, Ale Nie Złożyli Zamówienia", [
        { "$match": { "items.0": { "$exists": True } } },
        {
            "$lookup": {
                "from": "orders",
                "let": { "uid": "$user_id" },
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$user_id", "$$uid"] } } },
                    { "$limit": 1 },
                    { "$project": { "_id": 1 } }
                ],
                "as": "existing_orders"
            }
        },
        { "$match": { "existing_orders": { "$size": 0 } } },
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_data"
            }
        },
        { "$unwind": "$user_data" },
        { "$unwind": "$items" },
        {
            "$lookup": {
                "from": "products",
                "localField": "items.product_id",
                "foreignField": "_id",
                "as": "product_info"
            }
        },
        { "$unwind": "$product_info" },
        {
            "$project": {
                "_id": 0,
                "user_email": "$user_data.email",
                "full_name": { "$concat": ["$user_data.first_name", " ", "$user_data.last_name"] },
                "abandoned_product": "$product_info.name",
                "cart_updated_at": "$updated_at"
            }
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

    22: ("Magazyny, Które Posiadają Zapasy Konkretnego Wariantu (np. variant_id=ObjectId)", [
        { "$match": { "$expr": { "$eq": ["$variant_id", { "$toObjectId": "{variant_id}" }] } } },
        {
            "$project": {
                "warehouse_id": 1,
                "quantity": "$quantity_on_hand"
            }
        },
        {
            "$unionWith": {
                "coll": "inventory_serial",
                "pipeline": [
                    { "$match": { "$expr": { "$eq": ["$variant_id", { "$toObjectId": "{variant_id}" }] } } },
                    { "$project": { "warehouse_id": 1, "quantity": { "$literal": 1 } } }
                ]
            }
        },
        {
            "$lookup": {
                "from": "warehouses",
                "localField": "warehouse_id",
                "foreignField": "_id",
                "as": "warehouse"
            }
        },
        { "$unwind": "$warehouse" },
        {
            "$group": {
                "_id": "$warehouse.name",
                "stock_count": { "$sum": "$quantity" }
            }
        },
        { "$match": { "stock_count": { "$gt": 0 } } },
        { "$project": { "_id": 0, "warehouse_name": "$_id", "stock_count": 1 } }
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

   # działa dla małych ilości danych
    26: ("Porównanie Średniej Oceny dla Promowanych i Niepromowanych Produktów", [
        {
            "$addFields": {
                "is_promoted": {
                    "$gt": [
                        {
                            "$size": {
                                "$filter": {
                                    "input": "$variants",
                                    "as": "v",
                                    "cond": { "$gt": ["$$v.current_promotion", None] }
                                }
                            }
                        },
                        0
                    ]
                }
            }
        },
        {
            "$project": {
                "promotion_status": {
                    "$cond": ["$is_promoted", "Promowany", "Niepromowany"]
                }
            }
        },
        {
            "$lookup": {
                "from": "reviews",
                "localField": "_id",
                "foreignField": "product_id",
                "as": "review_docs"
            }
        },
        { "$match": { "review_docs.0": { "$exists": True } } },
        { "$unwind": "$review_docs" },
        {
            "$group": {
                "_id": "$promotion_status",
                "average_rating": { "$avg": "$review_docs.rating" },
                "total_reviews": { "$sum": 1 }
            }
        },
        {
            "$project": {
                "promotion_status": "$_id",
                "average_rating": { "$round": ["$average_rating", 2] },
                "total_reviews": 1,
                "_id": 0
            }
        }
    ]),

    27: ("Top 5 Miast Generujących Największy Przychód (Wg. Adresu Wysyłki)", [
        {"$group": {"_id": "$shipping_address.city", "city_revenue": {"$sum": "$total_amount"}}},
        {"$sort": {"city_revenue": -1}},
        {"$limit": 5}
    ]),

    28: ("Wskaźnik Lojalności (Repeat Purchase Rate) Użytkowników z Podziałem na Miasto Adresu Rozliczeniowego", [
        {"$group": {"_id": {"user_id": "$user_id", "city": "$billing_address.city"}, "orders_count": {"$sum": 1}}},
        {"$group": {"_id": "$_id.city", "repeat_customers": {"$sum": {"$cond": [{"$gt": ["$orders_count", 1]}, 1, 0]}}, "total_customers": {"$sum": 1}}},
        {"$project": {"repeat_purchase_rate": {"$cond": [ {"$eq": ["$total_customers", 0]}, 0, {"$round": [{"$multiply": [{"$divide": ["$repeat_customers", "$total_customers"]}, 100]}, 2]}]}, "repeat_customers": 1, "total_customers": 1}},
        {"$sort": {"repeat_purchase_rate": -1}}
    ])
    
    }
