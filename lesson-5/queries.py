# queries.py
QUERIES = {
    # Zapytania statystyczne i agregujące dla platformy e-commerce
    1: ("Średnia Wartość Zamówienia (AOV) w Ostatnim Miesiącu", """
         SELECT
        AVG(total_price)
        FROM (
            SELECT
            o.id,
            SUM(oi.unit_price * oi.quantity) AS total_price
            FROM "Order" o
            JOIN "OrderItem" oi ON o.id = oi.order_id
            WHERE o.order_date >= NOW() - INTERVAL '1 month'
            GROUP BY o.id
        ) AS monthly_orders;
    """),

    2: ("Średnia wartość zamówienia per użytkownik", """
        SELECT 
        u.id, 
        u.first_name, 
        u.last_name,
        ROUND(AVG(order_totals.total_price), 2) AS avg_order_value
        FROM "User" u
        JOIN "Order" o ON o.user_id = u.id
        JOIN (
            SELECT 
                oi.order_id,
                SUM(oi.unit_price * oi.quantity) AS total_price
            FROM "OrderItem" oi
            GROUP BY oi.order_id
        ) AS order_totals ON order_totals.order_id = o.id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY avg_order_value DESC;
    """),

    3: ("Top 10 Najlepiej Sprzedających Się Produktów (wg. Ilości Sprzedanych Jednostek) w Ostatnim Kwartale", """
        SELECT
        p.name AS product_name,
        m.name AS manufacturer_name,
        SUM(oi.quantity) AS total_units_sold
        FROM "Product" p
        JOIN "Manufacturer" m ON p.manufacturer_id = m.id
        JOIN "Variant" v ON v.product_id = p.id
        JOIN "OrderItem" oi ON oi.variant_id = v.id
        JOIN "Order" o ON oi.order_id = o.id
        WHERE o.order_date >= NOW() - INTERVAL '3 months'
        GROUP BY p.name, m.name
        ORDER BY total_units_sold DESC
        LIMIT 10;
    """),

    4: ("Top 5 produktów z najwięcej recenzjami", """
        SELECT p.id, p.name, COUNT(r.id) AS reviews_count
        FROM "Product" p
        LEFT JOIN "Review" r ON r.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY reviews_count DESC
        LIMIT 5;
    """),
    
    5: ("Całkowity Przychód Pogrupowany Miesięcznie za Ostatni Rok", """
        SELECT
        DATE_TRUNC('month', o.order_date)::date AS order_month,
        SUM(oi.unit_price * oi.quantity) AS monthly_revenue
        FROM "Order" o
        JOIN "OrderItem" oi ON o.id = oi.order_id
        WHERE o.order_date >= NOW() - INTERVAL '1 year'
        GROUP BY order_month
        ORDER BY order_month DESC;
    """),
    
    6: ("Produkty najczęściej dodawane do ulubionych", """
        SELECT p.id, p.name, COUNT(f.id) AS favorites_count
        FROM "Product" p
        JOIN "FavoriteProduct" f ON f.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY favorites_count DESC
        LIMIT 10;
    """),

    7: ("Dostępny Stan Magazynowy Wariantów Produktu Pogrupowany po Magazynach", """
        SELECT
        p.name AS product_name,
        v.sku,
        w.name AS warehouse_name,
        COUNT(si.id) AS stock_count
        FROM "StockItem" si
        JOIN "Variant" v ON si.variant_id = v.id
        JOIN "Product" p ON v.product_id = p.id
        JOIN "Warehouse" w ON si.warehouse_id = w.id
        WHERE si.shipment_id IS NULL 
        GROUP BY p.name, v.sku, w.name
        ORDER BY p.name, w.name;
    """),

    8: ("Stan magazynowy per produkt", """
        SELECT p.name AS product_name, SUM(CASE WHEN si.shipment_id IS NULL THEN 1 ELSE 0 END) AS stock_count
        FROM "Product" p
        JOIN "Variant" v ON v.product_id = p.id
        JOIN "StockItem" si ON si.variant_id = v.id
        GROUP BY p.name
        ORDER BY stock_count DESC;
    """),
    
    9: ("Najpopularniejsze Kategorie (wg. Całkowitego Przychodu)", """
        SELECT
        c.name AS category_name,
        SUM(oi.unit_price * oi.quantity) AS total_category_revenue
        FROM "Category" c
        JOIN "ProductCategory" pc ON c.id = pc.category_id
        JOIN "Product" p ON pc.product_id = p.id
        JOIN "Variant" v ON p.id = v.product_id
        JOIN "StockItem" si ON v.id = si.variant_id
        JOIN "OrderItem" oi ON si.id = oi.stock_item_id
        GROUP BY c.name
        ORDER BY total_category_revenue DESC
        LIMIT 10;
    """),

     10: ("Liczba produktów per kategoria", """
        SELECT c.name AS category_name, COUNT(pc.product_id) AS products_count
        FROM "Category" c
        LEFT JOIN "ProductCategory" pc ON pc.category_id = c.id
        GROUP BY c.name
        ORDER BY products_count DESC;
    """),
#////////////////////////////////////////////////////////////////////////////////
    #Pośrednie pomiędzy statysztyczne a analityczne
    11: ("Liczba zamówień per metoda płatności", """
        SELECT pm.name AS payment_method, COUNT(o.id) AS orders_count, SUM(oi.unit_price * oi.quantity) AS total_value
        FROM "Order" o
        JOIN "PaymentMethod" pm ON pm.id = o.payment_method_id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY pm.name
        ORDER BY total_value DESC;
    """),

    12: ("Średnia ocena per producent", """
        SELECT m.name AS manufacturer, AVG(r.rating) AS avg_rating
        FROM "Manufacturer" m
        JOIN "Product" p ON p.manufacturer_id = m.id
        LEFT JOIN "Review" r ON r.product_id = p.id
        GROUP BY m.name
        ORDER BY avg_rating DESC NULLS LAST;
    """),

     13: ("Aktywne promocje i objęta nimi liczba wariantów", """
        SELECT pr.name AS promotion_name,
            COUNT(v.id) AS active_discount_items
        FROM "Promotion" pr
        JOIN "Variant" v ON v.promotion_id = pr.id
        WHERE pr.start_date <= NOW()
        AND pr.end_date >= NOW()
        GROUP BY pr.name
        ORDER BY active_discount_items DESC;
        """),

# ///////////////////////////////////////////////////////////////////////////////
    #Analityczne i optymalizacyjne
    14: ("Najczęściej wybierane warianty w koszykach", """
        SELECT v.sku, p.name AS product_name, SUM(ci.quantity) AS total_quantity
        FROM "CartItem" ci
        JOIN "Variant" v ON v.id = ci.variant_id
        JOIN "Product" p ON p.id = v.product_id
        GROUP BY v.sku, p.name
        ORDER BY total_quantity DESC
        LIMIT 10;
    """),
    15: ("Produkty z Największą Różnicą Między Ceną Podstawową a Ceną Wariantu", """
       SELECT
        p.name AS product_name,
        v.sku,
        p.price AS base_price,
        v.price_modifier AS discount_percentage,
        p.price * (1 - v.price_modifier / 100) AS final_variant_price
        FROM "Product" p
        JOIN "Variant" v ON p.id = v.product_id
        ORDER BY v.price_modifier DESC
        LIMIT 10;
    """),

    16: ("Konwersja zamówień wg statusu", """
        SELECT s.name AS status,
            COUNT(o.id) AS orders_count,
            ROUND(
                COUNT(o.id)::numeric / SUM(COUNT(o.id)) OVER () * 100,
                2
            ) AS percentage_share
        FROM "Order" o
        JOIN "Status" s ON s.id = o.status_id
        GROUP BY s.name
        ORDER BY orders_count DESC;
    """),

   17: ("Top klienci wg wydatków", """
        SELECT u.id, u.first_name, u.last_name, SUM(oi.unit_price * oi.quantity) AS total_spent
        FROM "User" u
        JOIN "Order" o ON o.user_id = u.id
        JOIN "OrderItem" oi ON oi.order_id = o.id
        GROUP BY u.id, u.first_name, u.last_name
        ORDER BY total_spent DESC
        LIMIT 10;
    """),

    18: ("Produkty z wariantami objętymi promocją, z końcową ceną", """
        SELECT p.name AS product_name, v.sku, 
                p.price * (1 + v.price_modifier / 100) AS final_price,
                pr.discount_percentage, 
                (p.price * (1 + v.price_modifier / 100)) * (1 - pr.discount_percentage / 100) AS discounted_price
        FROM "Variant" v
        JOIN "Product" p ON p.id = v.product_id
        JOIN "Promotion" pr ON pr.id = v.promotion_id
        WHERE pr.start_date <= NOW() AND pr.end_date >= NOW()
        ORDER BY discounted_price ASC;
    """),

     19: ("Użytkownicy, Którzy Dodali Produkt do Koszyka, Ale Nie Złożyli Zamówienia (Potencjał Odbudowy Koszyka)", """
       SELECT DISTINCT
        u.email,
        p.name AS product_in_cart
        FROM "User" u
        JOIN "Cart" c ON u.id = c.user_id
        JOIN "CartItem" ci ON c.id = ci.cart_id
        JOIN "Variant" v ON ci.variant_id = v.id
        JOIN "Product" p ON v.product_id = p.id
        LEFT JOIN "Order" o ON u.id = o.user_id
        WHERE o.id IS NULL;

    """),
#///////////////////////////////////////////////////////////////////////////////

    # Wyszukiwanie i kntestowe
     20: ("Wyszukiwanie produktów po nazwie lub opisie (parametryzowane)", """
        SELECT id, name, description, price
        FROM "Product"
        WHERE name ILIKE '%' || :search_term || '%' 
        OR description ILIKE '%' || :search_term || '%';

    """),

    21: ("Użytkownicy, Którzy Zapisali Konkretny Produkt jako Ulubiony (np. Product ID=350259)", """
        SELECT
        u.email,
        u.first_name,
        u.last_name
        FROM "User" u
        JOIN "FavoriteProduct" fp ON u.id = fp.user_id
        WHERE fp.product_id = 350259;
    """),

    22: ("Znajdź Magazyny, Które Posiadają Zapasy Konkretnego Wariantu (np. SKU='VR-000000-a637d44b7afd')", """
       SELECT
        w.name AS warehouse_name,
        COUNT(si.id) AS stock_count
        FROM "Warehouse" w
        JOIN "StockItem" si ON w.id = si.warehouse_id
        JOIN "Variant" v ON si.variant_id = v.id
        WHERE v.sku = 'VR-000000-a637d44b7afd' AND si.shipment_id IS NULL
        GROUP BY w.name
        HAVING COUNT(si.id) > 0;
    """),
    #To nie wiem czy działa
    24: ("Warianty, Które Wymagają Uzyskania Konkretnej Opcji (np. 'Kolor'='Czerwony')", """
        SELECT
        v.sku,
        p.name AS product_name
        FROM "Variant" v
        JOIN "Product" p ON v.product_id = p.id
        JOIN "VariantOption" vo ON v.id = vo.variant_id
        JOIN "Option" opt ON vo.option_id = opt.id
        JOIN "Attribute" a ON opt.attribute_id = a.id
        WHERE a.name = 'Kolor' AND opt.value = 'Czerwony';
    """),

    25: ("Znajdź Zamówienia Użytkownika (np. email='jan.kowalski@example.com') o Statusie 'W trakcie realizacji'", """
        SELECT
        o.id AS order_id,
        o.order_date,
        s.name AS status
        FROM "Order" o
        JOIN "User" u ON o.user_id = u.id
        JOIN "Status" s ON o.status_id = s.id
        WHERE u.email = 'jan.kowalski@example.com' AND s.name = 'W trakcie realizacji';
    """),

    26: ("Wszystkie Warianty i Ich Ceny dla Konkretnego Produktu (np. ID=350259)", """
        SELECT
        v.sku,
        a.name AS attribute_name,
        opt.value AS option_value,
        p.price AS base_price,
        v.price_modifier,
        p.price * (1 + v.price_modifier / 100) AS current_price
        FROM "Product" p
        JOIN "Variant" v ON p.id = v.product_id
        LEFT JOIN "VariantOption" vo ON v.id = vo.variant_id
        LEFT JOIN "Option" opt ON vo.option_id = opt.id
        LEFT JOIN "Attribute" a ON opt.attribute_id = a.id
        WHERE p.id = 350259;
    """),

    27: ("Lista Wszystkich Dziecięcych Kategorii (Podkategorii) dla Konkretnej Kategorii Nadrzędnej (np. ID=5)", """
        SELECT
        name
        FROM "Category"
        WHERE parent_id = 5;
    """),

#/////////////////////////////////////////////////////////////////////////////
    # Złożone i porównawcze

    28: ("Porównanie Średniej Oceny dla Promowanych i Niepromowanych Produktów", """
        SELECT
        promotion_status,
        AVG(avg_rating) AS average_rating
        FROM (
        SELECT
            p.id,
            CASE WHEN EXISTS (
                SELECT 1 FROM "Variant" v2 WHERE v2.product_id = p.id AND v2.promotion_id IS NOT NULL
            ) THEN 'Promowany' ELSE 'Niepromowany' END AS promotion_status,
            AVG(r.rating) AS avg_rating
        FROM "Product" p
        JOIN "Review" r ON p.id = r.product_id
        GROUP BY p.id
        ) sub
    GROUP BY promotion_status;
    """),

    29: ("Top 5 Miast Generujących Największy Przychód (Wg. Adresu Wysyłki)", """
        SELECT
        a.city,
        SUM(oi.unit_price * oi.quantity) AS city_revenue
        FROM "Address" a
        JOIN "Order" o ON a.id = o.shipping_address_id
        JOIN "OrderItem" oi ON o.id = oi.order_id
        GROUP BY a.city
        ORDER BY city_revenue DESC
        LIMIT 5;
    """),

    30: ("Porównanie Wolumenu Sprzedaży Produktów Promowanych vs. Niepromowanych (w Ostatnich 30 Dniach)", """
        SELECT
        CASE WHEN v.promotion_id IS NOT NULL THEN 'Promowany' ELSE 'Niepromowany' END AS promotion_status,
        SUM(oi.quantity) AS total_quantity_sold
        FROM "Order" o
        JOIN "OrderItem" oi ON o.id = oi.order_id
        JOIN "Variant" v ON oi.variant_id = v.id
        WHERE o.order_date >= NOW() - INTERVAL '30 days'
        GROUP BY promotion_status;
    """),

    31: ("Wskaźnik Lojalności (Repeat Purchase Rate) Użytkowników z Podziałem na Miasto Adresu Rozliczeniowego", """
        SELECT
            a.city,
            COUNT(DISTINCT CASE WHEN user_orders.orders_count > 1 THEN o.user_id END) AS repeat_customers,
            COUNT(DISTINCT o.user_id) AS total_customers,
            ROUND(
                COUNT(DISTINCT CASE WHEN user_orders.orders_count > 1 THEN o.user_id END) * 100.0 /
                NULLIF(COUNT(DISTINCT o.user_id), 0),
                2
            ) AS repeat_purchase_rate
        FROM "Order" o
        JOIN "Address" a ON o.billing_address_id = a.id
        JOIN (
            SELECT user_id, COUNT(*) AS orders_count
            FROM "Order"
            GROUP BY user_id
        ) AS user_orders ON user_orders.user_id = o.user_id
        GROUP BY a.city
        ORDER BY repeat_purchase_rate DESC;
    """),
}
