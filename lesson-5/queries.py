# queries.py
QUERIES = {
    1: ("Lista wszystkich użytkowników z adresem", """
        SELECT u.id, u.first_name, u.last_name, u.email, u.role,
               a.street, a.city, a.postal_code, a.country
        FROM "User" u
        LEFT JOIN "Address" a ON u.address_id = a.id
        ORDER BY u.last_name, u.first_name;
    """),
    2: ("Średnia wartość zamówienia per użytkownik", """
        SELECT u.id, u.first_name, u.last_name, AVG(oi.unit_price) AS avg_order_value
        FROM "User" u
        JOIN "Order" o ON o.user_id = u.id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY avg_order_value DESC;
    """),
    3: ("Lista produktów z producentem i kategoriami", """
        SELECT p.id, p.name, m.name AS manufacturer,
               string_agg(c.name, ', ') AS categories
        FROM "Product" p
        JOIN "Manufacturer" m ON p.manufacturer_id = m.id
        LEFT JOIN "ProductCategory" pc ON pc.product_id = p.id
        LEFT JOIN "Category" c ON c.id = pc.category_id
        GROUP BY p.id, p.name, m.name
        ORDER BY p.name;
    """),
    4: ("Średnia ocena produktów", """
        SELECT p.id, p.name, AVG(r.rating) AS avg_rating, COUNT(r.id) AS review_count
        FROM "Product" p
        LEFT JOIN "Review" r ON r.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY avg_rating DESC NULLS LAST;
    """),
    5: ("Top 5 produktów z najwięcej recenzjami", """
        SELECT p.id, p.name, COUNT(r.id) AS reviews_count
        FROM "Product" p
        LEFT JOIN "Review" r ON r.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY reviews_count DESC
        LIMIT 5;
    """),
    6: ("Produkty w promocji", """
        SELECT v.id AS variant_id, p.name AS product_name, pr.name AS promotion_name, pr.discount_percentage
        FROM "Variant" v
        JOIN "Product" p ON p.id = v.product_id
        JOIN "Promotion" pr ON pr.id = v.promotion_id
        WHERE pr.start_date <= NOW() AND pr.end_date >= NOW();
    """),
    7: ("Wartość zamówień z podziałem na status", """
        SELECT s.name AS status, COUNT(o.id) AS orders_count, SUM(oi.unit_price) AS total_value
        FROM "Order" o
        JOIN "Status" s ON s.id = o.status_id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY s.name
        ORDER BY total_value DESC;
    """),
    8: ("Produkty najczęściej dodawane do ulubionych", """
        SELECT p.id, p.name, COUNT(f.id) AS favorites_count
        FROM "Product" p
        JOIN "FavoriteProduct" f ON f.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY favorites_count DESC
        LIMIT 10;
    """),
    9: ("Produkty i warianty z ceną końcową", """
        SELECT p.name AS product_name, v.sku, v.price_modifier, v.price_modifier + p.price AS final_price
        FROM "Product" p
        JOIN "Variant" v ON v.product_id = p.id
        ORDER BY final_price DESC;
    """),
    10: ("Liczba wariantów i średnia cena per produkt", """
        SELECT p.id, p.name, COUNT(v.id) AS variants_count, AVG(v.price_modifier + p.price) AS avg_variant_price
        FROM "Product" p
        LEFT JOIN "Variant" v ON v.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY avg_variant_price DESC;
    """),
    11: ("Liczba produktów per kategoria", """
        SELECT c.name AS category_name, COUNT(pc.product_id) AS products_count
        FROM "Category" c
        LEFT JOIN "ProductCategory" pc ON pc.category_id = c.id
        GROUP BY c.name
        ORDER BY products_count DESC;
    """),
    12: ("Stan magazynowy per produkt", """
        SELECT p.name AS product_name, COUNT(si.id) AS stock_count
        FROM "Product" p
        JOIN "Variant" v ON v.product_id = p.id
        JOIN "StockItem" si ON si.variant_id = v.id
        GROUP BY p.name
        ORDER BY stock_count DESC;
    """),
    13: ("Liczba zamówień per metoda płatności", """
        SELECT pm.name AS payment_method, COUNT(o.id) AS orders_count, SUM(oi.unit_price) AS total_value
        FROM "Order" o
        JOIN "PaymentMethod" pm ON pm.id = o.payment_method_id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY pm.name
        ORDER BY total_value DESC;
    """),
    14: ("Średnia ocena per producent", """
        SELECT m.name AS manufacturer, AVG(r.rating) AS avg_rating
        FROM "Manufacturer" m
        JOIN "Product" p ON p.manufacturer_id = m.id
        LEFT JOIN "Review" r ON r.product_id = p.id
        GROUP BY m.name
        ORDER BY avg_rating DESC NULLS LAST;
    """),
    15: ("Najczęściej wybierane warianty w koszykach", """
        SELECT v.sku, p.name AS product_name, SUM(ci.quantity) AS total_quantity
        FROM "CartItem" ci
        JOIN "Variant" v ON v.id = ci.variant_id
        JOIN "Product" p ON p.id = v.product_id
        GROUP BY v.sku, p.name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """),
    16: ("Aktywne promocje i objęta nimi liczba wariantów", """
        SELECT pr.name AS promotion_name,
            COUNT(v.id) AS active_discount_items
        FROM "Promotion" pr
        JOIN "Variant" v ON v.promotion_id = pr.id
        WHERE pr.start_date <= NOW()
        AND pr.end_date >= NOW()
        GROUP BY pr.name
        ORDER BY active_discount_items DESC;
    """),
    17: ("Najaktywniejsi użytkownicy wg liczby recenzji", """
        SELECT u.id, u.first_name, u.last_name, COUNT(r.id) AS reviews_count
        FROM "User" u
        JOIN "Review" r ON r.user_id = u.id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY reviews_count DESC
        LIMIT 10;
    """),
    18: ("Wyszukiwanie produktów po nazwie lub opisie (parametryzowane)", """
        SELECT id, name, description, price
        FROM "Product"
        WHERE name ILIKE %s OR description ILIKE %s;
    """),
    19: ("Konwersja zamówień wg statusu", """
        SELECT s.name AS status,
            COUNT(o.id) AS orders_count,
            ROUND(
                COUNT(o.id)::numeric /
                SUM(COUNT(o.id)) OVER () * 100,
                2
            ) AS percentage_share
        FROM "Order" o
        JOIN "Status" s ON s.id = o.status_id
        GROUP BY s.name
        ORDER BY orders_count DESC;
    """),
    20: ("Produkty z wariantami objętymi promocją, z końcową ceną", """
        SELECT p.name AS product_name, v.sku, 
               v.price_modifier + p.price AS final_price,
               pr.discount_percentage, 
               (v.price_modifier + p.price) * (1 - pr.discount_percentage/100) AS discounted_price
        FROM "Variant" v
        JOIN "Product" p ON p.id = v.product_id
        JOIN "Promotion" pr ON pr.id = v.promotion_id
        WHERE pr.start_date <= NOW() AND pr.end_date >= NOW()
        ORDER BY discounted_price ASC;
    """),
    21: ("Top klienci wg wydatków", """
        SELECT u.id, u.first_name, u.last_name, SUM(oi.unit_price) AS total_spent
        FROM "User" u
        JOIN "Order" o ON o.user_id = u.id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """),
}
