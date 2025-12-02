## **1. Variant**

Variant(<u>id</u>, <i>product_id</i>, sku, price_modifier, <i>promotion_id</i>, unique_individual)

**Sprawdzenie:**
- **1NF**: Atrybuty są **atomowe**.
- **2NF**: Klucz główny jest **pojedynczy**.
- **3NF**: Wszystkie atrybuty zależą **bezpośrednio od klucza głównego**.

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **2. BulkStockItem**

BulkStockItem(<u>id</u>, <i>variant_id</i>, <i>warehouse_id</i>, <i>shipment_id</i>, quantity)

**Sprawdzenie:**
- **1NF**: Atrybuty są **atomowe**.
- **2NF**: Klucz główny jest **pojedynczy**.
- **3NF**: Wszystkie atrybuty opisują konkretny rekord zasobu masowego i zależą bezpośrednio od <u>id</u>.

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **3. SerialStockItem**

SerialStockItem(<u>id</u>, <i>shipment_id</i>, <i>warehouse_id</i>, <i>variant_id</i>, serial_number)

**Sprawdzenie:**
- **1NF**: Atrybuty są **atomowe**.
- **2NF**: Klucz główny jest **pojedynczy** (<u>id</u>), automatycznie spełnia 2NF.
- **3NF**: Wszystkie atrybuty opisują konkretny przedmiot z unikalnym numerem seryjnym i zależą bezpośrednio od <u>id</u>.

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## **4. OrderStockAllocation**

OrderStockAllocation(<u>id</u>, <i>order_item_id</i>, <i>bulk_stock_id</i>, <i>serial_stock_id</i>, allocated_quantity, allocate_at)

**Sprawdzenie:**
- **1NF**: Atrybuty są **atomowe**.
- **2NF**: Klucz główny jest **pojedynczy**.
- **3NF**: Wszystkie atrybuty opisują konkretną alokację zasobu na pozycję zamówienia i zależą bezpośrednio od <u>id</u>.

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.

---

## 5. OrderItem

**Schemat:** OrderItem(<u>id</u>, <i>order_id</i>, <i>variant_id</i>, unit_price, quantity)

**Sprawdzenie:**
- **1NF**: Atrybuty są **atomowe**.
- **2NF**: Klucz główny jest **pojedynczy**.
- **3NF**: Wszystkie atrybuty zależą **bezpośrednio od <u>id</u>** (konkretnej pozycji zamówienia).

**Wniosek:** Schemat jest w **3NF**, nie wymaga dekompozycji.