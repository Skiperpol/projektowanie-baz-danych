from __future__ import annotations
import csv
import io
import random
import time
from collections import defaultdict
from typing import Dict, List, Optional
from utils.db import DB
from .entities import ENTITY_LOADERS
from .entities.category_helper import CategoryHelper


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
        self.category_helper = CategoryHelper(self)
        random.seed(0)

    def _ensure_category_metadata(self):
        self.category_helper.ensure_category_metadata()

    def _initialize_category_metadata(self, category_rows):
        self.category_helper.initialize_category_metadata(category_rows)

    def _compute_category_depth(self, category_id: int) -> int:
        return self.category_helper.compute_category_depth(category_id)

    def _build_category_shared_attributes(self, attribute_ids: List[int]):
        self.category_helper.build_category_shared_attributes(attribute_ids)

    def _get_optional_attrs_for_category(self, category_id: int, attribute_ids: List[int]) -> List[int]:
        return self.category_helper.get_optional_attrs_for_category(category_id, attribute_ids)

    def _calculate_optional_count(self, shared_count: int) -> int:
        return self.category_helper.calculate_optional_count(shared_count)

    def _bound_optional_count(self, optional_count: int) -> int:
        return self.category_helper.bound_optional_count(optional_count)

    def _register_product_category_pair(self, product_id: int, category_id: int):
        self.category_helper.register_product_category_pair(product_id, category_id)

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

