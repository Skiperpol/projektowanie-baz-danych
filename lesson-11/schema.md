# warehouses

```
{
  "_id": "wh_central",
  "name": "Magazyn Centralny - Łódź",
  "address": {
    "street": "Magazynowa 15",
    "city": "Łódź",
    "postal_code": "90-001",
    "country": "PL"
  },
  "is_active": true
}
```

---

# products

```
{
  "_id": "prod_1001",
  "name": "Słuchawki Bezprzewodowe NoiseCancel",
  "description": "Wysokiej klasy słuchawki z redukcją szumów.",
  "manufacturer": {
    "id": 55,
    "name": "Sony"
  },
  "categories": [
    { "id": 10, "name": "Audio" },
    { "id": 20, "name": "Elektronika" }
  ],
  "base_attributes": {
    "warranty": "24 miesiące",
    "connection": "Bluetooth 5.0"
  },
  "avg_rating": { "$numberDecimal": "4.8" },
  "review_count": 124,
  "variants": [
    {
      "_id": { "$oid": "6580abc00000000000000001" },
      "sku": "SONY-NC-BLK",
      "base_price": { "$numberDecimal": "1200.00" },
      "attributes": { "color": "Black" },
      "inventory_type": "bulk",
      "current_promotion": { 
        "promo_id": "PROMO_WINTER_2025",
        "final_price": { "$numberDecimal": "1020.00" }
      }
    },
    {
      "_id": { "$oid": "6580abc00000000000000002" },
      "sku": "SONY-NC-SILVER",
      "base_price": { "$numberDecimal": "1250.00" },
      "attributes": { "color": "Silver" },
      "inventory_type": "bulk"
    }
  ]
}
```

---

# inventory_bulk

```
{
  "warehouse_id": "wh_central",
  "variant_id": { "$oid": "6580abc00000000000000001" },
  "quantity_on_hand": 100,
  "quantity_reserved": 2
}
```

---

# inventory_serial

```
{
  "serial_number": "SN-APPLE-999888777",
  "variant_id": { "$oid": "6580abc00000000000000001" },
  "warehouse_id": "wh_central",
  "status": "AVAILABLE",
  "history": [
    {
      "status": "RECEIVED",
      "date": { "$date": "2024-05-10T09:00:00Z" }
    }
  ]
}
```
---

# users

```
{
  "_id": "user_555",
  "first_name": "Jan",
  "last_name": "Kowalski",
  "email": "jan@kowalski.pl",
  "password_hash": "$2b$10$EixZAY...",
  "roles": ["user"],
  "addresses": [
    {
      "id": "addr_1",
      "street": "Prosta 10/5",
      "city": "Warszawa",
      "postal_code": "00-100",
      "country": "PL",
      "is_default_shipping": true
    }
  ],
  "registered_at": { "$date": "2023-11-20T14:30:00Z" },
  # "favorites_products": ["prod_1001"]
}
```

---

# carts (zakładamy ograniczenie na items)

```
{
  "user_id": "user_555",
  "updated_at": { "$date": "2025-12-17T12:00:00Z" },
  "items": [
    {
      "variant_id": { "$oid": "6580abc00000000000000001" },
      "product_id": "prod_1001",
      "quantity": 1
    }
  ]
}
```

---

# orders

```
{
  "_id": "order_2024_9001",
  "user_id": "user_555",
  "status": "PAID",
  "order_date": { "$date": "2025-12-17T12:05:00Z" },
  "shipping_address": {
    "street": "Prosta 10/5",
    "city": "Warszawa",
    "postal_code": "00-100",
    "country": "PL"
  },
  "billing_address": {
    "street": "Prosta 10/5",
    "city": "Warszawa",
    "postal_code": "00-100",
    "country": "PL"
  },
  "delivery_method": {
    "name": "Kurier DHL",
    "cost": { "$numberDecimal": "15.99" }
  },
  "payment_method": "BLIK",
  "total_amount": { "$numberDecimal": "1215.99" },
  "items": [
    {
      "product_id": "prod_1001",
      "variant_sku": "SONY-NC-BLK",
      "name": "Słuchawki Bezprzewodowe NoiseCancel (Czarny)",
      "quantity": 1,
      "unit_price": { "$numberDecimal": "1200.00" }
    }
  ]
}
```

---

# reviews

```
{
  "product_id": "prod_1001",
  "user_id": "user_555",
  "rating": 5,
  "comment": "Świetne słuchawki, polecam!",
  "posted_at": { "$date": "2025-12-20T10:00:00Z" },
  "helpful_votes": 12
}
```
---

# manufacturers

```
{
  "_id": 55,
  "name": "Sony",
  "description": "Japoński producent elektroniki użytkowej, lider w branży audio i wideo.",
  "website": "https://www.sony.com",
  "contact": {
    "email": "support@sony.pl",
    "phone": "+48 22 123 45 67"
  },
  "active": true
}
```

---

# user_favorites

```
{
  "_id": { "$oid": "6580abc00000000000000123" },
  "user_id": "user_555",
  "product_id": "prod_1001",
  "added_at": { "$date": "2025-12-17T12:00:00Z" }
}
```

# promotions

```
{
  "_id": "PROMO_WINTER_2025",
  "name": "Zimowa Wyprzedaż Audio",
  "is_active": true,
  "start_date": { "$date": "2025-12-01T00:00:00Z" },
  "end_date": { "$date": "2025-12-31T23:59:59Z" },
  "target": {
    "scope": "CATEGORY", // Opcje: "SINGLE_PRODUCT", "CATEGORY", "MANUFACTURER", "ALL"
    "target_id": 10
  },
  "discount": {
    "type": "PERCENTAGE", // lub "FIXED"
    "value": 15
  }
}
```