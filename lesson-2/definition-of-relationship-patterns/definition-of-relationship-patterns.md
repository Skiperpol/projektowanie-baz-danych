## **1. User**

User(<u>id</u>, first_name, last_name, email, password, role, <i>address_id</i>)


**Klucz główny:** `id`  
**Klucze obce:** `address_id` → `Address(id)`

**Zależności funkcyjne:**
- `id → first_name, last_name, email, password, role, address_id`
- `email → id` (email jest unikalny)

**Zależności wielowartościowe:** ∅

---

## **2. Address**

Address(<u>id</u>, street, city, postal_code, country)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → street, city, postal_code, country`

**Zależności wielowartościowe:** ∅

---

## **3. Status**

Status(<u>id</u>, name)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name`
- `name → id` (nazwa statusu jest unikalna)

**Zależności wielowartościowe:** ∅

---

## **4. Order**

Order(<u>id</u>, <i>user_id</i>, <i>delivery_method_id</i>, <i>payment_method_id</i>, order_date, 
      <i>status_id</i>, <i>billing_address_id</i>, <i>shipping_address_id</i>)


**Klucz główny:** `id`  
**Klucze obce:**
- `user_id` → `User(id)`
- `delivery_method_id` → `DeliveryMethod(id)`
- `payment_method_id` → `PaymentMethod(id)`
- `status_id` → `Status(id)`
- `billing_address_id` → `Address(id)`
- `shipping_address_id` → `Address(id)`

**Zależności funkcyjne:**
- `id → user_id, delivery_method_id, payment_method_id, order_date, status_id, billing_address_id, shipping_address_id`

**Zależności wielowartościowe:** ∅

---

## **5. DeliveryMethod**

DeliveryMethod(<u>id</u>, name, cost)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name, cost`

**Zależności wielowartościowe:** ∅

---

## **6. PaymentMethod**

PaymentMethod(<u>id</u>, name)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name`

**Zależności wielowartościowe:** ∅

---

## **7. OrderItem**

OrderItem(<u>id</u>, <i>order_id</i>, <i>stock_item_id</i>, unit_price)


**Klucz główny:** `id`  
**Klucze obce:**
- `order_id` → `Order(id)`
- `stock_item_id` → `StockItem(id)`

**Zależności funkcyjne:**
- `id → order_id, stock_item_id, unit_price`
- `stock_item_id → id` (każda sprzedana sztuka jest przypisana do jednej linii zamówienia)

**Zależności wielowartościowe:** ∅

---

## **8. Cart**

Cart(<u>id</u>, <i>user_id</i>)


**Klucz główny:** `id`  
**Klucze obce:** `user_id` → `User(id)`

**Zależności funkcyjne:**
- `id → user_id`
- `user_id → id` (relacja 1:1, każdy user ma jeden koszyk)

**Zależności wielowartościowe:** ∅

---

## **9. CartItem**

CartItem(<u>id</u>, <i>cart_id</i>, <i>variant_id</i>, quantity)


**Klucz główny:** `id`  
**Klucze obce:**
- `cart_id` → `Cart(id)`
- `variant_id` → `Variant(id)`

**Zależności funkcyjne:**
- `id → cart_id, variant_id, quantity`

**Zależności wielowartościowe:** ∅

---

## **10. Manufacturer**

Manufacturer(<u>id</u>, name)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name`

**Zależności wielowartościowe:** ∅

---

## **11. Product**

Product(<u>id</u>, <i>manufacturer_id</i>, name, description, price)


**Klucz główny:** `id`  
**Klucze obce:** `manufacturer_id` → `Manufacturer(id)`

**Zależności funkcyjne:**
- `id → manufacturer_id, name, description, price`

**Zależności wielowartościowe:** ∅

---

## **12. Category**

Category(<u>id</u>, name, <i>parent_id</i>)


**Klucz główny:** `id`  
**Klucze obce:** `parent_id` → `Category(id)` (relacja rekurencyjna)

**Zależności funkcyjne:**
- `id → name, parent_id`

**Zależności wielowartościowe:** ∅

---

## **13. ProductCategory**

ProductCategory(<u><i>product_id</i>, <i>category_id</i></u>)


**Klucz główny:** `(product_id, category_id)` - klucz złożony  
**Klucze obce:**
- `product_id` → `Product(id)`
- `category_id` → `Category(id)`

**Zależności funkcyjne:**
- `(product_id, category_id) → ∅` (brak dodatkowych atrybutów)

**Zależności wielowartościowe:**
- `product_id →→ category_id` (produkt może należeć do wielu kategorii)
- `category_id →→ product_id` (kategoria może zawierać wiele produktów)

---

## **14. Variant**

Variant(<u>id</u>, <i>product_id</i>, sku, price_modifier, <i>promotion_id</i>)


**Klucz główny:** `id`  
**Klucze obce:**
- `product_id` → `Product(id)`
- `promotion_id` → `Promotion(id)`

**Zależności funkcyjne:**
- `id → product_id, sku, price_modifier, promotion_id`
- `sku → id` (SKU jest unikalne)

**Zależności wielowartościowe:** ∅

---

## **15. Promotion**

Promotion(<u>id</u>, name, discount_percentage, start_date, end_date)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name, discount_percentage, start_date, end_date`

**Zależności wielowartościowe:** ∅

---

## **16. Attribute**

Attribute(<u>id</u>, name)


**Klucz główny:** `id`  
**Klucze obce:** brak

**Zależności funkcyjne:**
- `id → name`

**Zależności wielowartościowe:** ∅

---

## **17. ProductAttribute**

ProductAttribute(<u><i>product_id</i>, <i>attribute_id</i></u>)


**Klucz główny:** `(product_id, attribute_id)`  
**Klucze obce:**
- `product_id` → `Product(id)`
- `attribute_id` → `Attribute(id)`

**Zależności funkcyjne:**
- `(product_id, attribute_id) → ∅`

**Zależności wielowartościowe:**
- `product_id →→ attribute_id` (produkt może mieć wiele atrybutów)
- `attribute_id →→ product_id` (atrybut może być przypisany do wielu produktów)

---

## **18. Option**

Option(<u>id</u>, <i>attribute_id</i>, value)


**Klucz główny:** `id`  
**Klucze obce:** `attribute_id` → `Attribute(id)`

**Zależności funkcyjne:**
- `id → attribute_id, value`

**Zależności wielowartościowe:** ∅

---

## **19. VariantOption**

VariantOption(<u><i>variant_id</i>, <i>option_id</i></u>)


**Klucz główny:** `(variant_id, option_id)`  
**Klucze obce:**
- `variant_id` → `Variant(id)`
- `option_id` → `Option(id)`

**Zależności funkcyjne:**
- `(variant_id, option_id) → ∅`

**Zależności wielowartościowe:**
- `variant_id →→ option_id` (wariant może mieć wiele opcji)
- `option_id →→ variant_id` (opcja może być w wielu wariantach)

---

## **20. Warehouse**

Warehouse(<u>id</u>, name, <i>address_id</i>)


**Klucz główny:** `id`  
**Klucze obce:** `address_id` → `Address(id)`

**Zależności funkcyjne:**
- `id → name, address_id`

**Zależności wielowartościowe:** ∅

---

## **21. StockItem**

StockItem(<u>id</u>, <i>variant_id</i>, <i>shipment_id</i>, <i>warehouse_id</i>)


**Klucz główny:** `id`  
**Klucze obce:**
- `variant_id` → `Variant(id)`
- `shipment_id` → `Shipment(id)`
- `warehouse_id` → `Warehouse(id)`

**Zależności funkcyjne:**
- `id → variant_id, shipment_id, warehouse_id`

**Zależności wielowartościowe:** ∅

---

## **22. Shipment**

Shipment(<u>id</u>, <i>order_id</i>, tracking_number, shipped_at)


**Klucz główny:** `id`  
**Klucze obce:** `order_id` → `Order(id)`

**Zależności funkcyjne:**
- `id → order_id, tracking_number, shipped_at`
- `tracking_number → id` (numer śledzenia jest unikalny)

**Zależności wielowartościowe:** ∅

---

## **23. Review**

Review(<u><i>user_id</i>, <i>product_id</i></u>, description, rating, posted_at)


**Klucz główny:** `(user_id, product_id)` - klucz złożony  
**Klucze obce:**
- `user_id` → `User(id)`
- `product_id` → `Product(id)`

**Zależności funkcyjne:**
- `(user_id, product_id) → description, rating, posted_at`

**Zależności wielowartościowe:** ∅

---

## **24. FavoriteProduct**

FavoriteProduct(<u><i>user_id</i>, <i>product_id</i></u>)


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