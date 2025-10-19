## **1. User**

User(<u>id</u>, first_name, last_name, email, password, role, <i>address_id</i>)

**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy (id), więc nie ma częściowych zależności funkcyjnych
- **3NF**: Brak zależności przechodnich (wszystkie atrybuty zależą bezpośrednio od id)

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **2. Address**

Address(<u>id</u>, street, city, postal_code, country, created_at, updated_at)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **3. Status**

Status(<u>id</u>, name)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **4. Order**

Order(<u>id</u>, <i>user_id</i>, <i>delivery_method_id</i>, <i>payment_method_id</i>, order_date, 
      <i>status_id</i>, <i>billing_address_id</i>, <i>shipping_address_id</i>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Wszystkie atrybuty zależą bezpośrednio od id, brak zależności przechodnich (klucze obce odnoszą się do innych tabel)

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **5. DeliveryMethod**

DeliveryMethod(<u>id</u>, name, cost)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **6. PaymentMethod**

PaymentMethod(<u>id</u>, name)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **7. OrderItem**

OrderItem(<u>id</u>, <i>order_id</i>, <i>stock_item_id</i>, quantity, unit_price)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Wszystkie atrybuty zależą bezpośrednio od id

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **8. Cart**

Cart(<u>id</u>, <i>user_id</i>, created_at)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **9. CartItem**

CartItem(<u>id</u>, <i>cart_id</i>, <i>variant_id</i>, quantity)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **10. Manufacturer**

Manufacturer(<u>id</u>, name)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **11. Product**

Product(<u>id</u>, <i>manufacturer_id</i>, name, description, price)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Wszystkie atrybuty zależą bezpośrednio od id

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **12. Category**

Category(<u>id</u>, name, <i>parent_id</i>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **13. ProductCategory**

ProductCategory(<u><i>product_id</i>, <i>category_id</i></u>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Brak atrybutów niekluczowych, więc automatycznie spełnia 2NF
- **3NF**: Brak zależności przechodnich (tabela zawiera tylko klucze)

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **14. Variant**

Variant(<u>id</u>, <i>product_id</i>, sku, price_modifier, <i>promotion_id</i>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Wszystkie atrybuty zależą bezpośrednio od id

**Uwaga:** Istnieje dodatkowa zależność `sku → id`, ale to nie narusza 3NF (kandydat na klucz alternatywny).

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **15. Promotion**

Promotion(<u>id</u>, name, discount_percentage, start_date, end_date)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **16. Attribute**

Attribute(<u>id</u>, name)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **17. ProductAttribute**

ProductAttribute(<u><i>product_id</i>, <i>attribute_id</i></u>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Brak atrybutów niekluczowych
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **18. Option**

Option(<u>id</u>, <i>attribute_id</i>, value)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **19. VariantOption**

VariantOption(<u><i>variant_id</i>, <i>option_id</i></u>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Brak atrybutów niekluczowych
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **20. Warehouse**

Warehouse(<u>id</u>, name, address)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe (address jako VARCHAR jest atomowy)
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

**Uwaga:** Gdybyśmy chcieli bardziej znormalizować, moglibyśmy rozbić `address` na osobną tabelę (jak w przypadku User i Order), ale to nie jest wymagane dla 3NF.

---

## **21. StockItem**

StockItem(<u>id</u>, <i>variant_id</i>, quantity, <i>shipment_id</i>, <i>warehouse_id</i>)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Wszystkie atrybuty zależą bezpośrednio od id

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **22. Shipment**

Shipment(<u>id</u>, <i>order_id</i>, tracking_number, shipped_at)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Klucz główny jest pojedynczy
- **3NF**: Brak zależności przechodnich

**Uwaga:** `tracking_number → id` to dodatkowa zależność, ale nie narusza 3NF (kandydat na klucz).

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **23. Review**

Review(<u><i>user_id</i>, <i>product_id</i></u>, description, rating, posted_at)


**Sprawdzenie:**
- **1NF**: Wszystkie atrybuty są atomowe
- **2NF**: Wszystkie atrybuty niekluczowe zależą od całego klucza złożonego
- **3NF**: Brak zależności przechodnich

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **24. FavoriteProduct**
```
FavoriteProduct(<u><i>user_id</i>, <i>product_id</i></u>)
```

**Klucz główny:** `(user_id, product_id)`  
**Klucze obce:**
- `user_id` → `User(id)`
- `product_id` → `Product(id)`

**Zależności funkcyjne:**
- `(user_id, product_id) → ∅`

**Zależności wielowartościowe:**
- `user_id →→ product_id` (użytkownik może mieć wiele ulubionych produktów)
- `product_id →→ user_id` (produkt może być ulubiony u wielu użytkowników)

---