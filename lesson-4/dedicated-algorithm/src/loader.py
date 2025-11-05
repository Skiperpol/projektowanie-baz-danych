import io
import csv
import json
import time
import random
from typing import Dict, List
from db import DB
from generator import *

class StreamLoader:
    def __init__(self, db: DB, row_counts: Dict[str,int]):
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
        random.seed(0)

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
                print(f"  Progress: {self.rows_inserted_per_table[table_name]:,} rows inserted for {table_name}")
            
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

    def load_all(self):
        order = [
            ('Category', ['name']),
            ('Address', ['street','city','postal_code','country']),
            ('Warehouse', ['name','address_id']),
            ('Attribute', ['name']),
            ('Option', ['attribute_id','value']),
            ('Manufacturer', ['name']),
            ('Promotion', ['name','discount_percentage','start_date','end_date']),
            ('Product', ['manufacturer_id','name','description','price']),
            ('Variant', ['product_id','sku','price_modifier','promotion_id']),
            ('StockItem', ['shipment_id','warehouse_id','variant_id']),
            ('User', ['first_name','last_name','email','password','role','address_id']),
            ('DeliveryMethod', ['name','cost']),
            ('PaymentMethod', ['name']),
            ('Status', ['name']),
            ('Cart', ['user_id']),
            ('CartItem', ['quantity','cart_id','variant_id']),
            ('Order', ['status_id','user_id','delivery_method_id','payment_method_id','order_date','billing_address_id','shipping_address_id']),
            ('OrderItem', ['order_id','stock_item_id','unit_price']),
            ('Shipment', ['order_id','tracking_number','shipped_at']),
            ('FavoriteProduct', ['user_id','product_id']),
            ('ProductCategory', ['product_id','category_id']),
            ('ProductAttribute', ['product_id','attribute_id']),
            ('VariantOption', ['variant_id','option_id']),
            ('Review', ['user_id','product_id','description','rating','posted_at']),
        ]
        batch = self.db.batch_size

        for table_name, columns in order:
            count = int(self.row_counts.get(table_name, 0))
            if count <= 0:
                print(f"Skipping {table_name}")
                continue
            print(f"\n=== Loading {table_name}: {count} rows ===")
            start = time.time()
            loader = getattr(self, f"_load_{table_name.lower()}", None)
            if loader:
                loader(table_name, columns, count, batch)
            else:
                self._load_generic(table_name, columns, count, batch)
            elapsed = time.time() - start
            print(f"-> Done {table_name} in {elapsed:.1f}s")

    def _load_generic(self, table_name, columns, count, batch):
        gen_fn = globals().get(f"gen_{table_name.lower()}_row")
        def rows():
            for i in range(count):
                yield tuple('' for _ in columns)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids[table_name] = self._fetch_recent_ids(table_name, count)

    def _load_category(self, table_name, columns, count, batch):
        def rows():
            for i in range(count):
                yield (f"Category_{i+1}",)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Category'] = self._fetch_recent_ids('Category', count)

    def _load_address(self, table_name, columns, count, batch):
        def rows():
            for _ in range(count):
                yield gen_address_row()
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Address'] = self._fetch_recent_ids('Address', count)

    def _load_manufacturer(self, table_name, columns, count, batch):
        if table_name not in self.unique_names:
            self.unique_names[table_name] = set()
        unique_set = self.unique_names[table_name]
        
        def rows():
            for i in range(count):
                self.unique_counter += 1
                yield gen_manufacturer_row(unique_set, self.unique_counter)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Manufacturer'] = self._fetch_recent_ids('Manufacturer', count)

    def _load_attribute(self, table_name, columns, count, batch):
        if table_name not in self.unique_names:
            self.unique_names[table_name] = set()
        unique_set = self.unique_names[table_name]
        
        def rows():
            for i in range(count):
                self.unique_counter += 1
                yield gen_attribute_row(unique_set, self.unique_counter)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Attribute'] = self._fetch_recent_ids('Attribute', count)

    def _load_option(self, table_name, columns, count, batch):
        attr_ids = self.generated_ids.get('Attribute', [])
        if not attr_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    aid = random.choice(attr_ids)
                    value = fake.word()
                    pair = (aid, value)
                    if pair not in self.option_pairs:
                        self.option_pairs.add(pair)
                        yield (aid, value)
                        break
                    attempt += 1
                else:
                    aid = random.choice(attr_ids)
                    value = f"Option_{i}_{random.randint(1000, 9999)}"
                    pair = (aid, value)
                    self.option_pairs.add(pair)
                    yield (aid, value)
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Option'] = self._fetch_recent_ids('Option', count)

    def _load_promotion(self, table_name, columns, count, batch):
        def rows():
            for _ in range(count):
                yield gen_promotion_row()
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Promotion'] = self._fetch_recent_ids('Promotion', count)

    def _load_product(self, table_name, columns, count, batch):
        man_ids = self.generated_ids.get('Manufacturer', [])
        if not man_ids:
            self._load_generic(table_name, columns, count, batch); return
        def rows():
            for _ in range(count):
                mid = random.choice(man_ids)
                yield gen_product_row(mid)
        self._copy_stream('public', table_name, columns, rows(), batch)
        prod_ids = self._fetch_recent_ids('Product', count)
        self.generated_ids['Product'] = prod_ids
        cur = self.ps_conn.cursor()
        cur.execute(f'SELECT id, price FROM "Product" ORDER BY id DESC LIMIT %s', (count,))
        rows = cur.fetchall(); cur.close()
        rows.reverse()
        for r in rows:
            self.product_price[r[0]] = str(r[1])

    def _load_variant(self, table_name, columns, count, batch):
        prod_ids = self.generated_ids.get('Product', [])
        promo_ids = self.generated_ids.get('Promotion', [])
        if not prod_ids:
            self._load_generic(table_name, columns, count, batch); return
        def rows():
            for _ in range(count):
                pid = random.choice(prod_ids)
                yield gen_variant_row(pid, promo_ids, self.unique_skus, self.sku_counter)
                self.sku_counter += 1
        self._copy_stream('public', table_name, columns, rows(), batch)
        var_ids = self._fetch_recent_ids('Variant', count)
        self.generated_ids['Variant'] = var_ids
        cur = self.ps_conn.cursor()
        cur.execute(f'SELECT id, product_id FROM "Variant" ORDER BY id DESC LIMIT %s', (count,))
        rows = cur.fetchall(); cur.close()
        rows.reverse()
        for r in rows:
            self.variant_to_product[r[0]] = r[1]

    def _load_warehouse(self, table_name, columns, count, batch):
        from constants import WAREHOUSE_VALUES
        
        addr_ids = self.generated_ids.get('Address', [])
        if not addr_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            for i in range(min(count, len(WAREHOUSE_VALUES))):
                name, predefined_address_id = WAREHOUSE_VALUES[i]
                if predefined_address_id <= len(addr_ids):
                    aid = addr_ids[predefined_address_id - 1]
                else:
                    aid = addr_ids[0] if addr_ids else None
                yield gen_warehouse_row(aid, None, i)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Warehouse'] = self._fetch_recent_ids('Warehouse', min(count, len(WAREHOUSE_VALUES)))

    def _load_stockitem(self, table_name, columns, count, batch):
        var_ids = self.generated_ids.get('Variant', [])
        wh_ids = self.generated_ids.get('Warehouse', [])
        if not var_ids or not wh_ids:
            self._load_generic(table_name, columns, count, batch); return
        def rows():
            for _ in range(count):
                wid = random.choice(wh_ids)
                vid = random.choice(var_ids)
                yield gen_stockitem_row(wid, vid)
        self._copy_stream('public', table_name, columns, rows(), batch)
        stock_ids = self._fetch_recent_ids('StockItem', count)
        self.generated_ids['StockItem'] = stock_ids
        cur = self.ps_conn.cursor()
        cur.execute(f'SELECT id, variant_id FROM "StockItem" ORDER BY id DESC LIMIT %s', (count,))
        rows = cur.fetchall(); cur.close()
        rows.reverse()
        for r in rows:
            sid, vid = r[0], r[1]
            self.stock_for_variant.setdefault(vid, []).append(sid)

    def _load_user(self, table_name, columns, count, batch):
        addr_ids = self.generated_ids.get('Address', [])
        def rows():
            for i in range(count):
                yield gen_user_row(addr_ids, self.unique_emails, self.email_counter)
                self.email_counter += 1
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['User'] = self._fetch_recent_ids('User', count)

    def _load_deliverymethod(self, table_name, columns, count, batch):
        from constants import DELIVERY_METHOD_VALUES
        
        def rows():
            for i in range(min(count, len(DELIVERY_METHOD_VALUES))):
                yield gen_delivery_method_row(i)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['DeliveryMethod'] = self._fetch_recent_ids('DeliveryMethod', min(count, len(DELIVERY_METHOD_VALUES)))

    def _load_paymentmethod(self, table_name, columns, count, batch):
        from constants import PAYMENT_METHOD_VALUES
        
        def rows():
            for i in range(min(count, len(PAYMENT_METHOD_VALUES))):
                yield gen_payment_method_row(i)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['PaymentMethod'] = self._fetch_recent_ids('PaymentMethod', min(count, len(PAYMENT_METHOD_VALUES)))

    def _load_status(self, table_name, columns, count, batch):
        from constants import STATUS_VALUES
        
        def rows():
            for i in range(min(count, len(STATUS_VALUES))):
                yield gen_status_row(i)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Status'] = self._fetch_recent_ids('Status', min(count, len(STATUS_VALUES)))

    def _load_cart(self, table_name, columns, count, batch):
        user_ids = self.generated_ids.get('User', [])
        if not user_ids:
            self._load_generic(table_name, columns, count, batch); return
        chosen = random.sample(user_ids, min(count, len(user_ids)))
        def rows():
            for uid in chosen:
                yield gen_cart_row(uid)
        self._copy_stream('public', table_name, columns, rows(), batch)
        cart_ids = self._fetch_recent_ids('Cart', len(chosen))
        self.generated_ids['Cart'] = cart_ids
        for u, c in zip(chosen, cart_ids):
            self.generated_ids.setdefault('user_to_cart_map', {})
            self.generated_ids['user_to_cart_map'][u] = c

    def _load_cartitem(self, table_name, columns, count, batch):
        cart_ids = self.generated_ids.get('Cart', [])
        var_ids = self.generated_ids.get('Variant', [])
        if not cart_ids or not var_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    cart = random.choice(cart_ids)
                    var = random.choice(var_ids)
                    pair = (cart, var)
                    if pair not in self.cartitem_pairs:
                        self.cartitem_pairs.add(pair)
                        qty = random.randint(1, 5)
                        yield gen_cartitem_row(cart, var, qty)
                        break
                    attempt += 1
                else:
                    print(f"  Warning: Could not generate unique (cart_id, variant_id) pair for CartItem row {i+1}")
                    cart = random.choice(cart_ids)
                    var = random.choice(var_ids)
                    pair = (cart, var)
                    self.cartitem_pairs.add(pair)
                    qty = random.randint(1, 5)
                    yield gen_cartitem_row(cart, var, qty)
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['CartItem'] = self._fetch_recent_ids('CartItem', count)

    def _load_order(self, table_name, columns, count, batch):
        user_ids = self.generated_ids.get('User', [])
        status_ids = self.generated_ids.get('Status', [])
        dm_ids = self.generated_ids.get('DeliveryMethod', [])
        pm_ids = self.generated_ids.get('PaymentMethod', [])
        addr_ids = self.generated_ids.get('Address', [])
        if not (user_ids and status_ids and dm_ids and pm_ids and addr_ids):
            self._load_generic(table_name, columns, count, batch); return
        def rows():
            for _ in range(count):
                uid = random.choice(user_ids)
                sid = random.choice(status_ids)
                dm = random.choice(dm_ids)
                pm = random.choice(pm_ids)
                bill = random.choice(addr_ids)
                ship = random.choice(addr_ids)
                order_date = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
                yield gen_order_row(sid, uid, dm, pm, bill, ship, order_date)
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Order'] = self._fetch_recent_ids('Order', count)

    def _load_orderitem(self, table_name, columns, count, batch):
        order_ids = self.generated_ids.get('Order', [])
        stock_ids = self.generated_ids.get('StockItem', [])
        if not order_ids or not stock_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    oid = random.choice(order_ids)
                    sid = random.choice(stock_ids)
                    pair = (oid, sid)
                    if pair not in self.orderitem_pairs:
                        self.orderitem_pairs.add(pair)
                        unit_price = str(Decimal(random.uniform(5, 500)).quantize(Decimal('0.01')))
                        yield gen_orderitem_row(oid, sid, unit_price)
                        break
                    attempt += 1
                else:
                    print(f"  Warning: Could not generate unique (order_id, stock_item_id) pair for OrderItem row {i+1}")
                    oid = random.choice(order_ids)
                    sid = random.choice(stock_ids)
                    pair = (oid, sid)
                    self.orderitem_pairs.add(pair)
                    unit_price = str(Decimal(random.uniform(5, 500)).quantize(Decimal('0.01')))
                    yield gen_orderitem_row(oid, sid, unit_price)
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['OrderItem'] = self._fetch_recent_ids('OrderItem', count)

    def _load_shipment(self, table_name, columns, count, batch):
        order_ids = self.generated_ids.get('Order', [])
        if not order_ids:
            self._load_generic(table_name, columns, count, batch); return
        def rows():
            for _ in range(count):
                oid = random.choice(order_ids)
                yield gen_shipment_row(oid, self.unique_tracking_numbers, self.tracking_counter)
                self.tracking_counter += 1
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Shipment'] = self._fetch_recent_ids('Shipment', count)

    def _load_favoriteproduct(self, table_name, columns, count, batch):
        user_ids = self.generated_ids.get('User', [])
        prod_ids = self.generated_ids.get('Product', [])
        if not user_ids or not prod_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    u = random.choice(user_ids)
                    p = random.choice(prod_ids)
                    pair = (u, p)
                    if pair not in self.favoriteproduct_pairs:
                        self.favoriteproduct_pairs.add(pair)
                        yield gen_favorite_row(u, p)
                        break
                    attempt += 1
                else:
                    print(f"  Warning: Could not generate unique (user_id, product_id) pair for FavoriteProduct row {i+1}")
                    u = random.choice(user_ids)
                    p = random.choice(prod_ids)
                    pair = (u, p)
                    self.favoriteproduct_pairs.add(pair)
                    yield gen_favorite_row(u, p)
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['FavoriteProduct'] = self._fetch_recent_ids('FavoriteProduct', count)

    def _load_simple_pair(self, table_name, columns, count, batch, left_ids_key, right_ids_key, gen_fn, pairs_set=None):
        left = self.generated_ids.get(left_ids_key, [])
        right = self.generated_ids.get(right_ids_key, [])
        if not left or not right:
            self._load_generic(table_name, columns, count, batch); return
        
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
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids[table_name] = self._fetch_recent_ids(table_name, count)

    def _load_productcategory(self, table_name, columns, count, batch):
        self._load_simple_pair('ProductCategory', columns, count, batch, 'Product', 'Category', gen_productcategory_row, self.productcategory_pairs)

    def _load_productattribute(self, table_name, columns, count, batch):
        self._load_simple_pair('ProductAttribute', columns, count, batch, 'Product', 'Attribute', gen_productattribute_row, self.productattribute_pairs)

    def _load_variantoption(self, table_name, columns, count, batch):
        self._load_simple_pair('VariantOption', columns, count, batch, 'Variant', 'Option', gen_variantoption_row, self.variantoption_pairs)

    def _load_review(self, table_name, columns, count, batch):
        user_ids = self.generated_ids.get('User', [])
        prod_ids = self.generated_ids.get('Product', [])
        if not user_ids or not prod_ids:
            self._load_generic(table_name, columns, count, batch); return
        
        def rows():
            max_attempts = 100
            for i in range(count):
                attempt = 0
                while attempt < max_attempts:
                    u = random.choice(user_ids)
                    p = random.choice(prod_ids)
                    pair = (u, p)
                    if pair not in self.review_pairs:
                        self.review_pairs.add(pair)
                        yield gen_review_row(u, p)
                        break
                    attempt += 1
                else:
                    print(f"  Warning: Could not generate unique (user_id, product_id) pair for Review row {i+1}")
                    u = random.choice(user_ids)
                    p = random.choice(prod_ids)
                    pair = (u, p)
                    self.review_pairs.add(pair)
                    yield gen_review_row(u, p)
        
        self._copy_stream('public', table_name, columns, rows(), batch)
        self.generated_ids['Review'] = self._fetch_recent_ids('Review', count)
