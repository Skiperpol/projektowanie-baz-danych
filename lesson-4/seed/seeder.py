import psycopg2
from io import StringIO
from typing import Dict, List, Any
from datetime import datetime, timedelta
from decimal import Decimal
import random
import logging
import time

from generator import get_faker_for_type, fake, reset_email_counter
from utils import escape_csv_value, columns_excluding_generated
from fk_resolver import find_table_dependencies
from data_domain import variant_price_from_product, shipment_date_for_order, posted_at_after_shipment

class Seeder:
    def __init__(self, tables: Dict[str, Any], order: List[str], db_cfg: Dict[str, Any], logger: logging.Logger = None):
        self.tables = tables
        self.order = order
        self.db_cfg = db_cfg
        self.logger = logger or logging.getLogger(__name__)
        self.generated_ids: Dict[str, List[int]] = {}
        self.sample_rows: Dict[str, List[Dict[str, Any]]] = {}
        self.review_pairs: set = set()
        self.orderitem_pairs: set = set()
        self.cartitem_pairs: set = set()
        self.favoriteproduct_pairs: set = set()
        self.productcategory_pairs: set = set()
        self.productattribute_pairs: set = set()
        self.variantoption_pairs: set = set()
        self.cart_user_ids: set = set()

    def _connect(self):
        conn = psycopg2.connect(
            host=self.db_cfg['host'],
            port=self.db_cfg['port'],
            user=self.db_cfg['user'],
            password=self.db_cfg['password'],
            database=self.db_cfg['database']
        )
        return conn

    def run(self):
        self.logger.info("Starting seeding of %d tables", len(self.order))
        for t in self.order:
            self.seed_table(t)
        self.logger.info("Seeding finished")

    def seed_table(self, table_name: str):
        table_info = self.tables[table_name]
        row_count = table_info.get("row_count", 0)
        batch_count = table_info.get("batch_count", 1) or 1
        columns = table_info.get("columns", [])
        copy_columns = columns_excluding_generated(columns)
        col_names = [c['name'] for c in copy_columns]
        col_str = ', '.join([f'"{c}"' for c in col_names])

        self.logger.info("Seeding %s: %d rows in %d batches", table_name, row_count, batch_count)
        fake.unique.clear()
        
        conn = self._connect()
        cur = conn.cursor()

        generated_ids_for_table = []
        batch_size = max(1, row_count // batch_count)
        start_time = time.time()
        for batch_idx in range(batch_count):
            if batch_idx < batch_count - 1:
                actual_batch = batch_size
            else:
                actual_batch = row_count - batch_size * (batch_count - 1)

            sio = StringIO()
            for _ in range(actual_batch):
                values = []
                generated_row = {}
                if table_name == "Review":
                    max_attempts = 100
                    attempt = 0
                    user_id = None
                    product_id = None
                    while attempt < max_attempts:
                        if "User" in self.generated_ids and self.generated_ids["User"]:
                            user_id = random.choice(self.generated_ids["User"])
                        if "Product" in self.generated_ids and self.generated_ids["Product"]:
                            product_id = random.choice(self.generated_ids["Product"])
                        pair = (user_id, product_id)
                        if pair not in self.review_pairs and user_id and product_id:
                            self.review_pairs.add(pair)
                            generated_row["user_id"] = user_id
                            generated_row["product_id"] = product_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (user_id, product_id) pair for Review after %d attempts", max_attempts)
                        generated_row["user_id"] = None
                        generated_row["product_id"] = None
                if table_name == "OrderItem":
                    max_attempts = 100
                    attempt = 0
                    order_id = None
                    stock_item_id = None
                    while attempt < max_attempts:
                        if "Order" in self.generated_ids and self.generated_ids["Order"]:
                            order_id = random.choice(self.generated_ids["Order"])
                        if "StockItem" in self.generated_ids and self.generated_ids["StockItem"]:
                            stock_item_id = random.choice(self.generated_ids["StockItem"])
                        pair = (order_id, stock_item_id)
                        if pair not in self.orderitem_pairs and order_id and stock_item_id:
                            self.orderitem_pairs.add(pair)
                            generated_row["order_id"] = order_id
                            generated_row["stock_item_id"] = stock_item_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (order_id, stock_item_id) pair for OrderItem after %d attempts", max_attempts)
                        generated_row["order_id"] = None
                        generated_row["stock_item_id"] = None
                if table_name == "Cart":
                    if "User" in self.generated_ids and self.generated_ids["User"]:
                        available_users = [uid for uid in self.generated_ids["User"] if uid not in self.cart_user_ids]
                        if available_users:
                            user_id = random.choice(available_users)
                            self.cart_user_ids.add(user_id)
                            generated_row["user_id"] = user_id
                        else:
                            self.logger.warning("No more available users for Cart. Skipping row.")
                            generated_row["user_id"] = None
                    else:
                        generated_row["user_id"] = None
                if table_name == "CartItem":
                    max_attempts = 100
                    attempt = 0
                    cart_id = None
                    variant_id = None
                    while attempt < max_attempts:
                        if "Cart" in self.generated_ids and self.generated_ids["Cart"]:
                            cart_id = random.choice(self.generated_ids["Cart"])
                        if "Variant" in self.generated_ids and self.generated_ids["Variant"]:
                            variant_id = random.choice(self.generated_ids["Variant"])
                        pair = (cart_id, variant_id)
                        if pair not in self.cartitem_pairs and cart_id and variant_id:
                            self.cartitem_pairs.add(pair)
                            generated_row["cart_id"] = cart_id
                            generated_row["variant_id"] = variant_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (cart_id, variant_id) pair for CartItem after %d attempts", max_attempts)
                        generated_row["cart_id"] = None
                        generated_row["variant_id"] = None
                if table_name == "FavoriteProduct":
                    max_attempts = 100
                    attempt = 0
                    user_id = None
                    product_id = None
                    while attempt < max_attempts:
                        if "User" in self.generated_ids and self.generated_ids["User"]:
                            user_id = random.choice(self.generated_ids["User"])
                        if "Product" in self.generated_ids and self.generated_ids["Product"]:
                            product_id = random.choice(self.generated_ids["Product"])
                        pair = (user_id, product_id)
                        if pair not in self.favoriteproduct_pairs and user_id and product_id:
                            self.favoriteproduct_pairs.add(pair)
                            generated_row["user_id"] = user_id
                            generated_row["product_id"] = product_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (user_id, product_id) pair for FavoriteProduct after %d attempts", max_attempts)
                        generated_row["user_id"] = None
                        generated_row["product_id"] = None
                if table_name == "ProductCategory":
                    max_attempts = 100
                    attempt = 0
                    product_id = None
                    category_id = None
                    while attempt < max_attempts:
                        if "Product" in self.generated_ids and self.generated_ids["Product"]:
                            product_id = random.choice(self.generated_ids["Product"])
                        if "Category" in self.generated_ids and self.generated_ids["Category"]:
                            category_id = random.choice(self.generated_ids["Category"])
                        pair = (product_id, category_id)
                        if pair not in self.productcategory_pairs and product_id and category_id:
                            self.productcategory_pairs.add(pair)
                            generated_row["product_id"] = product_id
                            generated_row["category_id"] = category_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (product_id, category_id) pair for ProductCategory after %d attempts", max_attempts)
                        generated_row["product_id"] = None
                        generated_row["category_id"] = None
                if table_name == "ProductAttribute":
                    max_attempts = 100
                    attempt = 0
                    product_id = None
                    attribute_id = None
                    while attempt < max_attempts:
                        if "Product" in self.generated_ids and self.generated_ids["Product"]:
                            product_id = random.choice(self.generated_ids["Product"])
                        if "Attribute" in self.generated_ids and self.generated_ids["Attribute"]:
                            attribute_id = random.choice(self.generated_ids["Attribute"])
                        pair = (product_id, attribute_id)
                        if pair not in self.productattribute_pairs and product_id and attribute_id:
                            self.productattribute_pairs.add(pair)
                            generated_row["product_id"] = product_id
                            generated_row["attribute_id"] = attribute_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (product_id, attribute_id) pair for ProductAttribute after %d attempts", max_attempts)
                        generated_row["product_id"] = None
                        generated_row["attribute_id"] = None
                if table_name == "VariantOption":
                    max_attempts = 100
                    attempt = 0
                    variant_id = None
                    option_id = None
                    while attempt < max_attempts:
                        if "Variant" in self.generated_ids and self.generated_ids["Variant"]:
                            variant_id = random.choice(self.generated_ids["Variant"])
                        if "Option" in self.generated_ids and self.generated_ids["Option"]:
                            option_id = random.choice(self.generated_ids["Option"])
                        pair = (variant_id, option_id)
                        if pair not in self.variantoption_pairs and variant_id and option_id:
                            self.variantoption_pairs.add(pair)
                            generated_row["variant_id"] = variant_id
                            generated_row["option_id"] = option_id
                            break
                        attempt += 1
                    if attempt >= max_attempts:
                        self.logger.warning("Could not generate unique (variant_id, option_id) pair for VariantOption after %d attempts", max_attempts)
                        generated_row["variant_id"] = None
                        generated_row["option_id"] = None
                
                for col in copy_columns:
                    name = col['name']
                    if table_name == "Review" and name in ["user_id", "product_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "OrderItem" and name in ["order_id", "stock_item_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "Cart" and name == "user_id":
                        if name in generated_row:
                            continue
                    if table_name == "CartItem" and name in ["cart_id", "variant_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "FavoriteProduct" and name in ["user_id", "product_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "ProductCategory" and name in ["product_id", "category_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "ProductAttribute" and name in ["product_id", "attribute_id"]:
                        if name in generated_row:
                            continue
                    if table_name == "VariantOption" and name in ["variant_id", "option_id"]:
                        if name in generated_row:
                            continue
                    
                    cons = " ".join([c.upper() for c in col.get("constraints", [])])
                    is_fk = "FOREIGN" in cons or "REFERENCES" in cons
                    if is_fk:
                        ref_table = self._find_ref_table_from_constraints(col.get("constraints", []))
                        if ref_table and ref_table in self.generated_ids and self.generated_ids[ref_table]:
                            val = random.choice(self.generated_ids[ref_table])
                        else:
                            val = None
                        generated_row[name] = val
                    else:
                        gen = get_faker_for_type(col, table_name)
                        try:
                            val = gen() if gen else None
                        except Exception:
                            val = None
                        if table_name == "Variant" and name == "price_modifier":
                            val = Decimal(str(round(random.uniform(0, 400), 2)))
                        if table_name == "Product" and name == "price":
                            val = Decimal(str(round(random.uniform(5, 2000), 2)))
                        if table_name == "Order" and name == "order_date":
                            val = fake.date_time_between(start_date='-180d', end_date='now')
                        if table_name == "Shipment" and name == "shipped_at":
                            val = fake.date_time_between(start_date='-90d', end_date='now')
                        if table_name == "Promotion" and name == "start_date":
                            val = fake.date_time_between(start_date='-2y', end_date='now')
                        if table_name == "Promotion" and name == "end_date":
                            start = generated_row.get("start_date")
                            if start:
                                min_end = start + timedelta(days=1)
                                max_end = start + timedelta(days=365)
                                val = fake.date_time_between(start_date=min_end, end_date=max_end)
                            else:
                                val = fake.date_time_between(start_date='-1y', end_date='now')
                        generated_row[name] = val

                for col in copy_columns:
                    v = generated_row.get(col['name'])
                    sio.write(escape_csv_value(v))
                    if col != copy_columns[-1]:
                        sio.write(',')
                sio.write('\n')

            sio.seek(0)
            copy_sql = f'COPY "{table_name}" ({col_str}) FROM STDIN WITH CSV NULL \'\\N\''
            try:
                cur.copy_expert(copy_sql, sio)
                conn.commit()
            except Exception as e:
                conn.rollback()
                self.logger.exception("COPY failed for %s batch %d: %s", table_name, batch_idx+1, e)
                raise

            try:
                cur.execute(f'SELECT id FROM "{table_name}" ORDER BY id DESC LIMIT %s', (actual_batch,))
                rows = cur.fetchall()
                new_ids = [r[0] for r in rows]
                new_ids = sorted(new_ids)
                generated_ids_for_table.extend(new_ids)
                cur.execute(f"SELECT * FROM \"{table_name}\" ORDER BY id DESC LIMIT %s", (min(10, actual_batch),))
                sample = cur.fetchall()
                self.sample_rows[table_name] = sample
                self.logger.info("  ✓ %s batch %d/%d: %d rows (IDs: %s - %s)",
                                 table_name, batch_idx+1, batch_count, actual_batch,
                                 min(new_ids) if new_ids else 'N/A', max(new_ids) if new_ids else 'N/A')
            except Exception as e:
                self.logger.exception("Failed to fetch IDs for %s: %s", table_name, e)
                raise

        self.generated_ids[table_name] = generated_ids_for_table
        elapsed = time.time() - start_time
        self.logger.info("✅ Finished %s: %d rows in %.2fs", table_name, len(generated_ids_for_table), elapsed)
        cur.close()
        conn.close()

    def _find_ref_table_from_constraints(self, constraints):
        for c in constraints:
            up = c.upper()
            if "REFERENCES" in up:
                parts = c.split()
                for i, p in enumerate(parts):
                    if p.upper() == "REFERENCES" and i+1 < len(parts):
                        return parts[i+1].strip().strip('();"')
            if "FOREIGN KEY" in up:
                m = None
                import re
                m = re.search(r'FOREIGN\s+KEY\s*\(\s*([A-Za-z0-9_"]+)\s*\)', c, re.IGNORECASE)
                if m:
                    return m.group(1).strip().strip('"')
        return None
