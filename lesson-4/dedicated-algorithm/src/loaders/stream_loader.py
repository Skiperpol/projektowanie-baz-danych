from __future__ import annotations

import csv
import io
import os
import random
import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from db import DB
from .entities import ENTITY_LOADERS


class StreamLoader:
    def __init__(self, db: DB, row_counts: Dict[str, int]):
        self.db = db
        self.row_counts = row_counts
        self.ps_conn = self.db.psycopg2_conn()
        self.generated_ids: Dict[str, List[int]] = {}
        self.product_price: Dict[int, str] = {}
        self.variant_to_product: Dict[int, int] = {}
        self.stock_for_variant: Dict[int, List[int]] = {}
        self.rows_inserted_per_table: Dict[str, int] = {}
        self.unique_names: Dict[str, set] = {}
        self.unique_counter = 0
        self.option_pairs: set = set()
        self.cartitem_pairs: set = set()
        self.orderitem_pairs: set = set()
        self.favoriteproduct_pairs: set = set()
        self.productcategory_pairs: set = set()
        self.productattribute_pairs: set = set()
        self.variantoption_pairs: set = set()
        self.review_pairs: set = set()
        self.unique_skus: set = set()
        self.sku_counter = 0
        self.unique_emails: set = set()
        self.email_counter = 0
        self.unique_tracking_numbers: set = set()
        self.tracking_counter = 0
        self.category_parent: Dict[int, Optional[int]] = {}
        self.category_children: Dict[int, List[int]] = defaultdict(list)
        self.category_depth: Dict[int, int] = {}
        self.category_order_cache: List[int] = []
        self.category_shared_attributes: Dict[int, List[int]] = {}
        self.category_optional_pool: Dict[int, List[int]] = {}
        self.category_products_map: Dict[int, List[int]] = defaultdict(list)
        self.product_to_categories: Dict[int, List[int]] = defaultdict(list)
        self.common_attribute_ratio = self._clamp_float(
            os.getenv("COMMON_ATTRIBUTE_RATIO"), 0.8, 0.1, 0.95
        )
        self.common_attribute_variation = self._clamp_float(
            os.getenv("COMMON_ATTRIBUTE_VARIATION"), 0.05, 0.0, 0.2
        )
        self.root_shared_attr_range = self._parse_range(
            os.getenv("ROOT_SHARED_ATTRIBUTE_RANGE"), (2, 4)
        )
        self.child_additional_attr_range = self._parse_range(
            os.getenv("CHILD_ADDITIONAL_ATTRIBUTE_RANGE"), (1, 2)
        )
        self.product_optional_attr_range = self._parse_range(
            os.getenv("PRODUCT_OPTIONAL_ATTRIBUTE_RANGE"), (0, 10)
        )
        self.optional_pool_size = max(0, int(os.getenv("CATEGORY_OPTIONAL_POOL_SIZE", "8")))
        random.seed(0)

    @staticmethod
    def _clamp_float(value: Optional[str], default: float, min_value: float, max_value: float) -> float:
        if value is None:
            return max(min(default, max_value), min_value)
        try:
            parsed = float(value)
        except ValueError:
            parsed = default
        return max(min(parsed, max_value), min_value)

    @staticmethod
    def _parse_range(value: Optional[str], default: Tuple[int, int]) -> Tuple[int, int]:
        if not value:
            return default
        parts = [p.strip() for p in value.split(",") if p.strip()]
        if len(parts) != 2:
            return default
        try:
            start, end = int(parts[0]), int(parts[1])
        except ValueError:
            return default
        if start > end:
            start, end = end, start
        if start < 0:
            start = 0
        return (start, end)

    def _ensure_category_metadata(self):
        if self.category_parent:
            return
        cur = self.ps_conn.cursor()
        cur.execute('SELECT id, parent_id FROM "Category"')
        rows = cur.fetchall()
        cur.close()
        self._initialize_category_metadata(rows)

    def _initialize_category_metadata(self, category_rows: List[Tuple[int, Optional[int]]]):
        self.category_parent = {}
        self.category_children = defaultdict(list)
        for cid, parent_id in category_rows:
            self.category_parent[cid] = parent_id
            if parent_id is not None:
                self.category_children[parent_id].append(cid)
        self.category_depth = {}
        for cid in self.category_parent:
            self._compute_category_depth(cid)
        self.category_order_cache = sorted(
            self.category_parent.keys(), key=lambda c: self.category_depth.get(c, 0)
        )
        self.category_shared_attributes = {}
        self.category_optional_pool = {}

    def _compute_category_depth(self, category_id: int) -> int:
        if category_id in self.category_depth:
            return self.category_depth[category_id]
        parent_id = self.category_parent.get(category_id)
        if parent_id is None:
            depth = 0
        else:
            depth = 1 + self._compute_category_depth(parent_id)
        self.category_depth[category_id] = depth
        return depth

    def _build_category_shared_attributes(self, attribute_ids: List[int]):
        if self.category_shared_attributes or not attribute_ids:
            return
        if not self.category_parent:
            self._ensure_category_metadata()
        for category_id in self.category_order_cache:
            parent_id = self.category_parent.get(category_id)
            parent_shared_list = self.category_shared_attributes.get(parent_id, [])
            parent_attrs = set(parent_shared_list)
            range_to_use = (
                self.root_shared_attr_range if parent_id is None else self.child_additional_attr_range
            )
            min_extra, max_extra = range_to_use
            extra_count = random.randint(min_extra, max_extra) if max_extra > 0 else 0
            available = [aid for aid in attribute_ids if aid not in parent_attrs]
            if len(available) < extra_count:
                available = attribute_ids[:]
            extra_attrs = random.sample(available, extra_count) if extra_count > 0 and available else []
            combined = list(dict.fromkeys([*parent_shared_list, *extra_attrs]))
            if not combined and attribute_ids:
                combined = [random.choice(attribute_ids)]
            self.category_shared_attributes[category_id] = combined

    def _get_optional_attrs_for_category(self, category_id: int, attribute_ids: List[int]) -> List[int]:
        if category_id not in self.category_optional_pool:
            shared = set(self.category_shared_attributes.get(category_id, []))
            pool_candidates = [aid for aid in attribute_ids if aid not in shared]
            if len(pool_candidates) < self.optional_pool_size:
                pool_candidates = attribute_ids[:]
            if self.optional_pool_size == 0 or not pool_candidates:
                pool = []
            else:
                unique_candidates = list(dict.fromkeys(pool_candidates))
                sample_size = min(self.optional_pool_size, len(unique_candidates))
                pool = random.sample(unique_candidates, sample_size)
            self.category_optional_pool[category_id] = pool
        return self.category_optional_pool[category_id]

    def _calculate_optional_count(self, shared_count: int) -> int:
        if shared_count == 0:
            return 0
        lower = max(self.common_attribute_ratio - self.common_attribute_variation, 0.01)
        upper = min(self.common_attribute_ratio + self.common_attribute_variation, 0.99)
        if lower > upper:
            lower, upper = upper, lower
        ratio = random.uniform(lower, upper)
        ratio = max(min(ratio, 0.95), 0.05)
        optional = round(shared_count * (1 - ratio) / ratio)
        return max(optional, 0)

    def _bound_optional_count(self, optional_count: int) -> int:
        min_val, max_val = self.product_optional_attr_range
        optional_count = max(optional_count, min_val)
        optional_count = min(optional_count, max_val)
        return optional_count

    def _register_product_category_pair(self, product_id: int, category_id: int):
        pair = (product_id, category_id)
        self.productcategory_pairs.add(pair)
        self.category_products_map[category_id].append(product_id)
        self.product_to_categories[product_id].append(category_id)

    def _copy_stream(self, table_schema: str, table_name: str, columns: List[str], rows_iter, batch: int):
        cur = self.ps_conn.cursor()
        buf = io.StringIO()
        writer = csv.writer(buf)
        written = 0
        if table_name not in self.rows_inserted_per_table:
            self.rows_inserted_per_table[table_name] = 0

        for row in rows_iter:
            writer.writerow(row)
            written += 1
            self.rows_inserted_per_table[table_name] += 1

            if self.rows_inserted_per_table[table_name] % 100000 == 0:
                print(
                    f"  Progress: {self.rows_inserted_per_table[table_name]:,} rows inserted for {table_name}"
                )

            if written % batch == 0:
                buf.seek(0)
                copy_sql = f'COPY "{table_name}" ({",".join(columns)}) FROM STDIN WITH CSV'
                cur.copy_expert(copy_sql, buf)
                self.ps_conn.commit()
                buf = io.StringIO()
                writer = csv.writer(buf)
        if buf.tell() > 0:
            buf.seek(0)
            copy_sql = f'COPY "{table_name}" ({",".join(columns)}) FROM STDIN WITH CSV'
            cur.copy_expert(copy_sql, buf)
            self.ps_conn.commit()
        cur.close()

    def _fetch_recent_ids(self, table_name: str, n: int) -> List[int]:
        cur = self.ps_conn.cursor()
        cur.execute(f'SELECT id FROM "{table_name}" ORDER BY id DESC LIMIT %s', (n,))
        rows = cur.fetchall()
        cur.close()
        ids = [r[0] for r in rows]
        ids.reverse()
        return ids

    def _load_generic(self, table_name, columns, count, batch):
        def rows():
            for _ in range(count):
                yield tuple("" for _ in columns)

        self._copy_stream("public", table_name, columns, rows(), batch)
        self.generated_ids[table_name] = self._fetch_recent_ids(table_name, count)

    def load_simple_pair(
        self,
        table_name,
        columns,
        count,
        batch,
        left_ids_key,
        right_ids_key,
        gen_fn,
        pairs_set=None,
    ):
        left = self.generated_ids.get(left_ids_key, [])
        right = self.generated_ids.get(right_ids_key, [])
        if not left or not right:
            self._load_generic(table_name, columns, count, batch)
            return

        if pairs_set is None:
            pairs_set = set()

        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    l = random.choice(left)
                    r = random.choice(right)
                    pair = (l, r)
                    if pair not in pairs_set:
                        pairs_set.add(pair)
                        yield gen_fn(l, r)
                        break
                    attempt += 1
                else:
                    print(f"  Warning: Could not generate unique pair for {table_name} row {i+1}")
                    l = random.choice(left)
                    r = random.choice(right)
                    pair = (l, r)
                    pairs_set.add(pair)
                    yield gen_fn(l, r)

        self._copy_stream("public", table_name, columns, rows(), batch)
        self.generated_ids[table_name] = self._fetch_recent_ids(table_name, count)

    def load_all(self):
        order = [
            ("Category", ["name", "parent_id"]),
            ("Address", ["street", "city", "postal_code", "country"]),
            ("Warehouse", ["name", "address_id"]),
            ("Attribute", ["name"]),
            ("Option", ["attribute_id", "value"]),
            ("Manufacturer", ["name"]),
            ("Promotion", ["name", "discount_percentage", "start_date", "end_date"]),
            ("Product", ["manufacturer_id", "name", "description", "price"]),
            ("Variant", ["product_id", "sku", "price_modifier", "promotion_id"]),
            ("StockItem", ["shipment_id", "warehouse_id", "variant_id"]),
            ("User", ["first_name", "last_name", "email", "password", "role", "address_id"]),
            ("DeliveryMethod", ["name", "cost"]),
            ("PaymentMethod", ["name"]),
            ("Status", ["name"]),
            ("Cart", ["user_id"]),
            ("CartItem", ["quantity", "cart_id", "variant_id"]),
            ("Order", ["status_id", "user_id", "delivery_method_id", "payment_method_id", "order_date", "billing_address_id", "shipping_address_id"]),
            ("OrderItem", ["order_id", "stock_item_id", "unit_price"]),
            ("Shipment", ["order_id", "tracking_number", "shipped_at"]),
            ("FavoriteProduct", ["user_id", "product_id"]),
            ("ProductCategory", ["product_id", "category_id"]),
            ("ProductAttribute", ["product_id", "attribute_id"]),
            ("VariantOption", ["variant_id", "option_id"]),
            ("Review", ["user_id", "product_id", "description", "rating", "posted_at"]),
        ]
        batch = self.db.batch_size

        for table_name, columns in order:
            count = int(self.row_counts.get(table_name, 0))
            if count <= 0:
                print(f"Skipping {table_name}")
                continue
            print(f"\n=== Loading {table_name}: {count} rows ===")
            start = time.time()
            loader_fn = ENTITY_LOADERS.get(table_name.lower().replace(" ", ""))
            if loader_fn:
                loader_fn(self, table_name, columns, count, batch)
            else:
                self._load_generic(table_name, columns, count, batch)
            elapsed = time.time() - start
            print(f"-> Done {table_name} in {elapsed:.1f}s")

