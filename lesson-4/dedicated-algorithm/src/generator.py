from faker import Faker
import random
import uuid
from decimal import Decimal
from datetime import timedelta
from typing import Optional, List, Tuple

fake = Faker()
Faker.seed(0)
random.seed(0)

USER_ROLES = ['user', 'admin', 'warehouseman', 'editor']

def gen_address_row():
    return (
        fake.street_address().replace(',', ' '),
        fake.city().replace(',', ' '),
        fake.postcode().replace(',', ' '),
        fake.country().replace(',', ' ')
    )

def gen_manufacturer_row(unique_set: set = None, counter: int = 0):
    """Generate unique manufacturer name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Man_{counter}_{unique_id}_{fake.company()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name,)
        unique_id = str(uuid.uuid4())[:8]
        name = f"Man_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name,)
    return (fake.company().replace(',', ' '),)

def gen_category_row(name_hint: Optional[str] = None):
    name = name_hint or fake.word().capitalize().replace(',', ' ')
    return (name,)

def gen_attribute_row(unique_set: set = None, counter: int = 0):
    """Generate unique attribute name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Attr_{counter}_{unique_id}_{fake.word().capitalize()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name,)
        unique_id = str(uuid.uuid4())[:8]
        name = f"Attr_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name,)
    return (fake.word().capitalize().replace(',', ' '),)

def gen_option_row(attribute_id: int):
    return (attribute_id, fake.word().replace(',', ' '))

def gen_promotion_row():
    start = fake.date_time_between(start_date='-1y', end_date='now')
    end = start + timedelta(days=random.randint(7, 180))
    discount = round(random.uniform(0.0, 50.0), 2)
    return (fake.word().capitalize().replace(',', ' '), str(discount), start.isoformat(), end.isoformat())

def gen_product_row(manufacturer_id: int):
    price = str(Decimal(random.uniform(5, 500)).quantize(Decimal('0.01')))
    name = (fake.word().capitalize() + ' ' + fake.word().capitalize()).replace(',', ' ')
    desc = fake.sentence(nb_words=6).replace(',', ' ')
    return (manufacturer_id, name, desc, price)

def gen_variant_row(product_id: int, promotion_ids: List[int], unique_skus: set = None, counter: int = 0):
    """Generate unique SKU for variant"""
    if unique_skus is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4()).replace('-', '')[:12]
            sku = f"VR-{counter:06d}-{unique_id}"
            if sku not in unique_skus:
                unique_skus.add(sku)
                price_modifier = str(Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')))
                promotion = random.choice(promotion_ids) if promotion_ids and random.random() < 0.12 else ''
                return (product_id, sku, price_modifier, promotion)
        unique_id = str(uuid.uuid4()).replace('-', '')[:12]
        sku = f"VR-{counter:06d}-{unique_id}"
        unique_skus.add(sku)
        price_modifier = str(Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')))
        promotion = random.choice(promotion_ids) if promotion_ids and random.random() < 0.12 else ''
        return (product_id, sku, price_modifier, promotion)
    sku = fake.unique.bothify(text='VR-????-#####')
    price_modifier = str(Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')))
    promotion = random.choice(promotion_ids) if promotion_ids and random.random() < 0.12 else ''
    return (product_id, sku, price_modifier, promotion)

def gen_warehouse_row(address_id: int, unique_set: set = None, counter: int = 0):
    """Generate unique warehouse name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Warehouse_{counter}_{unique_id}_{fake.company()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name, address_id)
        unique_id = str(uuid.uuid4())[:8]
        name = f"Warehouse_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name, address_id)
    return (fake.company().replace(',', ' '), address_id)

def gen_stockitem_row(warehouse_id: int, variant_id: int):
    return ('', warehouse_id, variant_id)

def gen_user_row(address_ids: List[int], unique_emails: set = None, counter: int = 0):
    """Generate unique email for user"""
    fn = fake.first_name().replace(',', ' ')
    ln = fake.last_name().replace(',', ' ')
    
    if unique_emails is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            email = f"{fn}.{ln}.{counter}.{unique_id}@example.com".lower().replace(' ', '')
            if email not in unique_emails:
                unique_emails.add(email)
                pw = fake.password(length=12)
                role = random.choice(USER_ROLES)
                address = random.choice(address_ids) if address_ids and random.random() < 0.8 else ''
                return (fn, ln, email, pw, role, address)
        unique_id = str(uuid.uuid4())[:8]
        email = f"user.{counter}.{unique_id}@example.com".lower()
        unique_emails.add(email)
        pw = fake.password(length=12)
        role = random.choice(USER_ROLES)
        address = random.choice(address_ids) if address_ids and random.random() < 0.8 else ''
        return (fn, ln, email, pw, role, address)
    
    email = f"{fn}.{ln}.{counter}@example.com".lower().replace(' ', '')
    pw = fake.password(length=12)
    role = random.choice(USER_ROLES)
    address = random.choice(address_ids) if address_ids and random.random() < 0.8 else ''
    return (fn, ln, email, pw, role, address)

def gen_delivery_method_row(unique_set: set = None, counter: int = 0):
    """Generate unique delivery method name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Delivery_{counter}_{unique_id}_{fake.word().capitalize()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name, str(round(random.uniform(0, 20),2)))
        unique_id = str(uuid.uuid4())[:8]
        name = f"Delivery_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name, str(round(random.uniform(0, 20),2)))
    return (fake.word().capitalize().replace(',', ' '), str(round(random.uniform(0, 20),2)))

def gen_payment_method_row(unique_set: set = None, counter: int = 0):
    """Generate unique payment method name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Payment_{counter}_{unique_id}_{fake.word().capitalize()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name,)
        unique_id = str(uuid.uuid4())[:8]
        name = f"Payment_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name,)
    return (fake.word().capitalize().replace(',', ' '),)

def gen_status_row(unique_set: set = None, counter: int = 0):
    """Generate unique status name"""
    if unique_set is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4())[:8]
            name = f"Status_{counter}_{unique_id}_{fake.word().capitalize()}".replace(',', ' ')[:100]
            if name not in unique_set:
                unique_set.add(name)
                return (name,)
        unique_id = str(uuid.uuid4())[:8]
        name = f"Status_{counter}_{unique_id}_{random.randint(1000, 9999)}"
        unique_set.add(name)
        return (name,)
    return (fake.word().capitalize().replace(',', ' '),)

def gen_cart_row(user_id: int):
    return (user_id,)

def gen_cartitem_row(cart_id: int, variant_id: int, quantity: int):
    return (quantity, cart_id, variant_id)

def gen_order_row(status_id: int, user_id: int, delivery_method_id: int, payment_method_id: int, billing_address_id: int, shipping_address_id: int, order_date_iso: str):
    return (status_id, user_id, delivery_method_id, payment_method_id, order_date_iso, billing_address_id, shipping_address_id)

def gen_orderitem_row(order_id: int, stock_item_id: int, unit_price: str):
    return (order_id, stock_item_id, unit_price)

def gen_shipment_row(order_id: int, unique_tracking_numbers: set = None, counter: int = 0):
    """Generate unique tracking number for shipment"""
    if unique_tracking_numbers is not None:
        max_attempts = 100
        for _ in range(max_attempts):
            unique_id = str(uuid.uuid4()).replace('-', '')[:12]
            tracking = f"TN-{counter:08d}-{unique_id}"
            if tracking not in unique_tracking_numbers:
                unique_tracking_numbers.add(tracking)
                shipped_at = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
                return (order_id, tracking, shipped_at)
        unique_id = str(uuid.uuid4()).replace('-', '')[:12]
        tracking = f"TN-{counter:08d}-{unique_id}"
        unique_tracking_numbers.add(tracking)
        shipped_at = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
        return (order_id, tracking, shipped_at)
    tracking = fake.unique.bothify(text='TN-########')
    shipped_at = fake.date_time_between(start_date='-1y', end_date='now').isoformat()
    return (order_id, tracking, shipped_at)

def gen_favorite_row(user_id: int, product_id: int):
    return (user_id, product_id)

def gen_productcategory_row(product_id: int, category_id: int):
    return (product_id, category_id)

def gen_productattribute_row(product_id: int, attribute_id: int):
    return (product_id, attribute_id)

def gen_variantoption_row(variant_id: int, option_id: int):
    return (variant_id, option_id)

def gen_review_row(user_id: int, product_id: int):
    rating = random.randint(1,5)
    posted = fake.date_time_between(start_date='-2y', end_date='now').isoformat()
    return (user_id, product_id, fake.sentence(nb_words=8).replace(',', ' '), rating, posted)
