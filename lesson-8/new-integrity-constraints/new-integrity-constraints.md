### Proponowane Nowe Więzy Integralności

#### 1. **Variant**

* **Ograniczenie Unikalności** (`UNIQUE`) na kolumnie `sku`.
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `price_modifier`, upewniające się, że wartość jest **większa lub równa 0**.
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `unique_individual`, wymuszające, że wartość jest poprawną wartością logiczną (np. `CHECK(unique_individual IN (0, 1))`).

#### 2. **BulkStockItem**

* **Ograniczenie Unikalności Kompozytowej** (`UNIQUE`) na kolumnach (`variant_id`, `warehouse_id`).
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `quantity`, wymuszające, że ilość jednostek jest **większa lub równa 0**.

#### 3. **SerialStockItem**

* **Ograniczenie Unikalności Kompozytowej** (`UNIQUE`) na kolumnach (`variant_id`, `serial_number`).

#### 4. **OrderStockAllocation**

* **Ograniczenie Sprawdzające** (`CHECK`), które gwarantuje, że **tylko jedna** z kolumn (`bulk_stock_id` lub `serial_stock_id`) jest wypełniona.
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `allocated_quantity`, upewniające się, że wartość jest **większa niż 0**.
* **Ograniczenie Unikalności Kompozytowej** (`UNIQUE`) na kolumnach (`order_item_id`, `bulk_stock_id`, `serial_stock_id`).

#### 5. **OrderItem**

* **Ograniczenie Unikalności Kompozytowej** (`UNIQUE`) na kolumnach (`order_id`, `variant_id`).
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `quantity`, wymuszające, że zamówiona ilość jest **większa lub równa 1**.
* **Ograniczenie Sprawdzające** (`CHECK`) na kolumnie `unit_price`, wymuszające, że cena jednostkowa jest **większa lub równa 0**.