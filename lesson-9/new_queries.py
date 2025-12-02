QUERIES = {
    # Zapytania statystyczne i agregujące
    1: ("Średnia Wartość Zamówienia (AOV) w Ostatnim Miesiącu", """
        SELECT
            AVG(total_price)
        FROM (
            SELECT
                o.id,
                SUM(oi.unit_price * oi.quantity) AS total_price -- Poprawiono: dodano quantity
            FROM "Order" o
            JOIN "OrderItem" oi ON o.id = oi.order_id
            WHERE o.order_date >= NOW() - INTERVAL '1 month'
            GROUP BY o.id
        ) AS monthly_orders;
    """),

    2: ("Średnia wartość zamówienia per użytkownik - ZOPTYMALIZOWANA", """
        SELECT 
            u.id, 
            u.first_name, 
            u.last_name,
            ROUND(AVG(oi_sum.total_price), 2) AS avg_order_value
        FROM "User" u
        JOIN "Order" o ON o.user_id = u.id
        JOIN (
            SELECT 
                order_id,
                SUM(unit_price * quantity) AS total_price
            FROM "OrderItem"
            GROUP BY order_id
        ) AS oi_sum ON oi_sum.order_id = o.id
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
        SELECT p.id, p.name, COALESCE(r.count, 0) AS reviews_count
        FROM "Product" p
        LEFT JOIN (
            SELECT product_id, COUNT(*) AS count
            FROM "Review"
            GROUP BY product_id
        ) r ON p.id = r.product_id
        ORDER BY reviews_count DESC
        LIMIT 5;

    """),
    
    5: ("Całkowity Przychód Pogrupowany Miesięcznie za Ostatni Rok", """
        SELECT
            DATE_TRUNC('month', order_date)::date AS order_month,
            SUM(unit_price * quantity) AS monthly_revenue
        FROM "OrderItem" oi
        JOIN "Order" o ON o.id = oi.order_id
        WHERE o.order_date >= NOW() - INTERVAL '1 year' -- Zmieniono na 1 rok
        GROUP BY 1
        ORDER BY 1 DESC;

    """),
    
    6: ("Produkty najczęściej dodawane do ulubionych", """
        SELECT p.id, p.name, COUNT(f.user_id) AS favorites_count
        FROM "Product" p
        JOIN "FavoriteProduct" f ON f.product_id = p.id
        GROUP BY p.id, p.name
        ORDER BY favorites_count DESC
        LIMIT 10;
    """),
    
    7: ("Dostępny Stan Magazynowy Wariantów Produktu Pogrupowany po Magazynach", """
        WITH AvailableStock AS (
            SELECT
                ssi.variant_id,
                ssi.warehouse_id,
                1 AS quantity 
            FROM "SerialStockItem" ssi
            
            UNION ALL
            
            SELECT
                bsi.variant_id,
                bsi.warehouse_id,
                bsi.quantity 
            FROM "BulkStockItem" bsi
        )
        
        SELECT
            p.name AS product_name,
            v.sku,
            w.name AS warehouse_name,
            SUM(astock.quantity) AS stock_count 
        FROM AvailableStock astock
        JOIN "Variant" v ON astock.variant_id = v.id
        JOIN "Product" p ON v.product_id = p.id
        JOIN "Warehouse" w ON astock.warehouse_id = w.id
        GROUP BY p.name, v.sku, w.name
        ORDER BY p.name, w.name;
    """),

    8: ("Stan magazynowy per produkt", """
        WITH ProductStock AS (
            SELECT
                v.product_id,
                1 AS quantity
            FROM "SerialStockItem" ssi
            JOIN "Variant" v ON ssi.variant_id = v.id
            
            UNION ALL
            
            SELECT
                v.product_id,
                bsi.quantity
            FROM "BulkStockItem" bsi
            JOIN "Variant" v ON bsi.variant_id = v.id
        )
        
        SELECT
            p.name AS product_name,
            SUM(ps.quantity) AS stock_count 
        FROM "Product" p
        JOIN ProductStock ps ON p.id = ps.product_id
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
        JOIN "OrderItem" oi ON v.id = oi.variant_id
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
        SELECT m.name AS manufacturer, ROUND(AVG(r.rating), 2) AS avg_rating
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
    #Analityczne  i optymalizacyjne
    14: ("Najczęściej wybierane warianty w koszykach", """
        WITH RankedCartItems AS (
            SELECT
                variant_id,
                SUM(quantity) AS total_quantity
            FROM "CartItem"
            GROUP BY variant_id
        )
        SELECT
            v.sku,
            p.name AS product_name,
            rci.total_quantity
        FROM RankedCartItems rci
        JOIN "Variant" v ON v.id = rci.variant_id
        JOIN "Product" p ON p.id = v.product_id   
        ORDER BY rci.total_quantity DESC
        LIMIT 10;
    """),

    15: ("Produkty z Największą Różnicą Między Ceną Podstawową a Ceną Wariantu", """
        SELECT
            p.name AS product_name,
            v.sku,
            p.price AS base_price,              
            p.price + v.price_modifier AS final_variant_price,
            v.price_modifier AS price_difference
        FROM "Product" p
        JOIN "Variant" v ON p.id = v.product_id
        ORDER BY price_difference DESC
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
                p.price + v.price_modifier AS final_price,
                pr.discount_percentage * 100 AS discount_percentage, 
                ROUND((p.price + v.price_modifier) * (1 - pr.discount_percentage), 2) AS discounted_price
        FROM "Variant" v
        JOIN "Product" p ON p.id = v.product_id
        JOIN "Promotion" pr ON pr.id = v.promotion_id
        WHERE pr.start_date <= NOW() AND pr.end_date >= NOW()
        ORDER BY discounted_price ASC;
    """),

    19: ("Użytkownicy, Którzy Dodali Produkt do Koszyka, Ale Nie Złożyli Zamówienia (Potencjał Odbudowy Koszyka)", """
        WITH users_without_orders AS (
            SELECT u.id, u.email
            FROM "User" u
            WHERE NOT EXISTS (
                SELECT 1
                FROM "Order" o
                WHERE o.user_id = u.id
            )
        )
        SELECT u.email, p.name AS product_in_cart
        FROM users_without_orders u
        JOIN "Cart" c ON u.id = c.user_id
        JOIN "CartItem" ci ON c.id = ci.cart_id
        JOIN "Variant" v ON ci.variant_id = v.id
        JOIN "Product" p ON v.product_id = p.id;
    """),
#///////////////////////////////////////////////////////////////////////////////
    # Wyszukiwanie i kntestowe

    20: ("Wyszukiwanie produktów po nazwie lub opisie (parametryzowane)", """
        SELECT id, name, description, price
        FROM "Product"
        WHERE name ILIKE %s 
        OR description ILIKE %s;
    """),

    21: ("Użytkownicy, Którzy Zapisali Konkretny Produkt jako Ulubiony (np. Product ID=350259)", """
        SELECT
        u.email,
        u.first_name,
        u.last_name
        FROM "User" u
        JOIN "FavoriteProduct" fp ON u.id = fp.user_id
        WHERE fp.product_id = 35;
    """),

    22: ("Znajdź Magazyny, Które Posiadają Zapasy Konkretnego Wariantu (np. SKU='VR-000000-a637d44b7afd')", """
        WITH VariantStock AS (
            SELECT
                bsi.warehouse_id,
                bsi.quantity AS stock_units
            FROM "BulkStockItem" bsi
            JOIN "Variant" v ON bsi.variant_id = v.id
            WHERE v.sku = 'VR-000001-2704de10f283'
            
            UNION ALL
            
            SELECT
                ssi.warehouse_id,
                1 AS stock_units 
            FROM "SerialStockItem" ssi
            JOIN "Variant" v ON ssi.variant_id = v.id
            WHERE v.sku = 'VR-000001-2704de10f283'
        )
        
        SELECT
            w.name AS warehouse_name,
            SUM(vs.stock_units) AS stock_count 
        FROM "Warehouse" w
        JOIN VariantStock vs ON w.id = vs.warehouse_id
        GROUP BY w.name
        HAVING SUM(vs.stock_units) > 0 
        ORDER BY stock_count DESC;
    """),

    23: ("Warianty, Które Wymagają Uzyskania Konkretnej Opcji (np. 'Kolor'='Czerwony')", """
        SELECT
        v.sku,
        p.name AS product_name
        FROM "Variant" v
        JOIN "Product" p ON v.product_id = p.id
        JOIN "VariantOption" vo ON v.id = vo.variant_id
        JOIN "Option" opt ON vo.option_id = opt.id
        JOIN "Attribute" a ON opt.attribute_id = a.id
        WHERE a.name = 'Attr_49_Century' AND opt.value = 'do';
    """),

    24: ("Znajdź Zamówienia Użytkownika (np. email='debbie.lane.16786.50af0753@example.com') o Statusie 'Paid'", """
        SELECT
        o.id AS order_id,
        o.order_date,
        s.name AS status
        FROM "Order" o
        JOIN "User" u ON o.user_id = u.id
        JOIN "Status" s ON o.status_id = s.id
        WHERE u.email = 'debbie.lane.16786.50af0753@example.com' AND s.name = 'Paid';
    """),

    25: ("Wszystkie Warianty i Ich Ceny dla Konkretnego Produktu (np. ID=350259)", """
        SELECT
        v.sku,
        a.name AS attribute_name,
        opt.value AS option_value,
        p.price AS base_price,
        v.price_modifier,
        p.price + v.price_modifier AS current_price
        FROM "Product" p
        JOIN "Variant" v ON p.id = v.product_id
        LEFT JOIN "VariantOption" vo ON v.id = vo.variant_id
        LEFT JOIN "Option" opt ON vo.option_id = opt.id
        LEFT JOIN "Attribute" a ON opt.attribute_id = a.id
        WHERE p.id = 35;
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
        SUM(oi.unit_price * oi.quantity) AS city_revenue -- Poprawiono: dodano quantity
        FROM "Address" a
        JOIN "Order" o ON a.id = o.shipping_address_id
        JOIN "OrderItem" oi ON o.id = oi.order_id
        GROUP BY a.city
        ORDER BY city_revenue DESC
        LIMIT 5;
    """),

    30: ("Porównanie Wolumenu Sprzedaży Produktów Promowanych vs. Niepromowanych (w Ostatnich 30 Dniach)", """
        SELECT
            CASE 
                WHEN v.promotion_id IS NOT NULL THEN 'Promowany' 
                ELSE 'Niepromowany' 
            END AS promotion_status,
            SUM(oi.quantity) AS total_units_sold 
        FROM "Order" o
        JOIN "OrderItem" oi ON o.id = oi.order_id
        JOIN "Variant" v ON oi.variant_id = v.id 
        WHERE o.order_date >= NOW() - INTERVAL '30 days'
        GROUP BY promotion_status;
    """),

    31: ("Wskaźnik Lojalności (Repeat Purchase Rate) Użytkowników z Podziałem na Miasto Adresu Rozliczeniowego", """
        WITH user_orders AS (
            SELECT user_id,
                    COUNT(*) AS orders_count
            FROM "Order"
            GROUP BY user_id
        ),
        orders_with_users AS (
            SELECT o.id, o.user_id, o.billing_address_id, u.orders_count
            FROM "Order" o
            JOIN user_orders u ON u.user_id = o.user_id
        )
        SELECT
            a.city,
            COUNT(*) FILTER (WHERE orders_count > 1) AS repeat_customers,
            COUNT(DISTINCT o.user_id) AS total_customers, -- Poprawiono: zliczanie unikalnych użytkowników
            ROUND(
                COUNT(*) FILTER (WHERE orders_count > 1) * 100.0 /
                NULLIF(COUNT(DISTINCT o.user_id), 0), -- Poprawiono: zliczanie unikalnych użytkowników
                2
            ) AS repeat_purchase_rate
        FROM orders_with_users o
        JOIN "Address" a ON a.id = o.billing_address_id
        GROUP BY a.city
        ORDER BY repeat_purchase_rate DESC;
    """),

}