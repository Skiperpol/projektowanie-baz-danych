## Zoptymalizowany Model MongoDB dla E-commerce


| \# | Nazwa Kolekcji | Zawartość | Uwagi |
| :--- | :--- | :--- | :--- |
| **1.** | **products** | Katalog, Warianty, Atrybuty, Promocje. | **Denormalizacja dla szybkiego odczytu.** |
| **2.** | **users** | Profil, Adresy, Role, Ulubione produkty (ID). | **Denormalizacja dla profilu użytkownika.** |
| **3.** | **orders** | Zamówienia, Pozycje, Status, Dostawa (Snapshot). | **Denormalizacja, dane historyczne (Snapshotting).** |
| **4.** | **warehouses** | Metadane Magazynów (Adresy, Nazwy). | **Nowa, mała kolekcja, referencyjna.** |
| **5.** | **inventory\_bulk** | Stan ilościowy (Bulk) dla każdego SKU w magazynie. | **Nowa kolekcja, wysoka częstotliwość aktualizacji.** |
| **6.** | **inventory\_serial** | Stan numerów seryjnych (Serial) i ich status. | **Nowa kolekcja, wysoka częstotliwość aktualizacji.** |
| **7.** | **reviews** | Opinie użytkowników. | **Osobna kolekcja ze względu na nieograniczony wzrost.** |
| **8.** | **carts** | Koszyki użytkowników (zastępuje logikę frontendu). | **Kluczowa dla transakcji i rezerwacji.** |

-----

## Szczegółowa Struktura Zoptymalizowanych Kolekcji

### 1\. Kolekcja `products`

(Denormalizacja tabel: Product, Manufacturer, Category, Variant, Promotion, etc.)

```json
{
  "_id": "prod_1001",
  "name": "Buty Biegowe X",
  "manufacturer": { "name": "Nike", "id": 10 },
  "categories": ["Obuwie", "Sport"],
  "variants": [
    {
      "sku": "NK-SHOE-42",
      "price": 299.99,
      "specs": { "Rozmiar": "42", "Kolor": "Niebieski" },
      "is_serial_tracked": false
    }
  ]
}
```

-----

### 2\. Kolekcja `users`

(Denormalizacja tabel: User, Address, Role, FavoriteProduct)

```json
{
  "_id": "user_555",
  "email": "jan@kowalski.pl",
  "favorite_product_ids": ["prod_1001", "prod_2005"]
}
```

-----

### 3\. Kolekcja `orders`

(Denormalizacja tabel: Order, OrderItem, Status, DeliveryMethod, PaymentMethod, Shipment)

```json
{
  "_id": "order_999",
  "user_id": "user_555",
  "status": "Wysłane",
  "delivery": {
    "method": "Kurier DHL",
    "shipping_address": { "street": "Polna 5", "city": "Warszawa" ... }
  },
  "items": [
    {
      "product_id": "prod_1001",
      "variant_sku": "NK-SHOE-42",
      "unit_price": 270.00,
      "quantity": 1
    }
  ]
}
```

-----

### 4\. Kolekcja `warehouses`

(Zastępuje tabelę: Warehouse - przechowuje tylko metadane)

```json
{
  "_id": "wh_centralny",
  "name": "Magazyn Główny",
  "address": { "street": "Magazynowa 1", "city": "Łódź" }
}
```

-----

### 5\. Kolekcja `inventory_bulk`

(Zastępuje logikę: BulkStockItem)

  * **Cel:** Śledzenie stanów ilościowych dla produktów nieśledzonych seryjnie.
  * **Wyszukiwanie:** Indeks na `warehouse_id` i `variant_sku`.
  * **Transakcje:** Używa operatora `$inc` (atomic increment) w transakcji wielodokumentowej do rezerwacji/sprzedaży.

```json
{
  "_id": ObjectId("65c58..."),
  "warehouse_id": "wh_centralny",
  "variant_sku": "NK-SHOE-42",
  "quantity_available": 50,
  "quantity_reserved": 2
}
```
-----

### 6\. Kolekcja `inventory_serial`

(Zastępuje logikę: SerialStockItem, OrderStockAllocation)

  * **Cel:** Śledzenie statusu każdego unikalnego numeru seryjnego.
  * **Wyszukiwanie:** Indeks na `serial_number`.
  * **Transakcje:** Atomowa aktualizacja statusu i przypisanie do zamówienia.

```json
{
  "_id": ObjectId("65c59..."),
  "warehouse_id": "wh_centralny",
  "variant_sku": "IPHONE-15-PRO",
  "serial_number": "SN12345",
  "status": "available",
  "reserved_by_order_id": null,
  "sold_in_order_id": null
}
```

-----

### 7\. Kolekcja `reviews`

(Zastępuje tabelę: Review)

```json
{
  "product_id": "prod_1001",
  "user_id": "user_555",
  "rating": 5,
  "text": "Super buty!"
}
```

### 8\. Kolekcja `carts`

(Zastępuje logikę logikę tabel Cart, CartItem)

  * **Cel:** Przechowuje aktualny stan koszyka i blokuje stan magazynowy (soft reservation).
  * **Wyszukiwanie:** Indeks na `user_id`.


```json
{
  "_id": "cart_888",
  "user_id": "user_555",
  "created_at": "2025-12-10T10:00:00Z",
  "items": [
    {
      "variant_sku": "NK-SHOE-42",
      "quantity": 1,
    },
  ]
}
```

## Podsumowanie Zalet Nowego Modelu

1.  **Wydajność Magazynu (Inventory):**
      * Rozbicie na `inventory_bulk` i `inventory_serial` eliminuje problem gigantycznych dokumentów, a tym samym **blokad całego magazynu** (contention).
      * Atomowe operacje na małych dokumentach SKU są znacznie szybsze i bezpieczniejsze.
2.  **Transakcje ACID:**
      * Krytyczna ścieżka **składania zamówienia** (Order Placement) może być teraz zaimplementowana za pomocą **transakcji wielodokumentowych MongoDB** obejmujących:
        1.  Usunięcie dokumentu `carts`.
        2.  Zmniejszenie `quantity_available` w `inventory_bulk` (lub zmiana statusu w `inventory_serial`).
        3.  Utworzenie dokumentu `orders`.
3.  **Precyzyjne Śledzenie Seryjne:**
      * Kolekcja `inventory_serial` umożliwia śledzenie historii konkretnej sztuki towaru, co jest zgodne z zaawansowaną logiką z Twojego oryginalnego schematu SQL (`SerialStockItem`).

Nowy model jest skalowalny, spójny w krytycznych momentach (dzięki transakcjom) i zapewnia błyskawiczny odczyt katalogu produktów.