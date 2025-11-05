from faker import Faker
import random
import uuid
from decimal import Decimal
from datetime import timedelta
from typing import Optional, List, Tuple
from constants import (
    USER_ROLES,
    STATUS_VALUES,
    PAYMENT_METHOD_VALUES,
    DELIVERY_METHOD_VALUES,
    WAREHOUSE_VALUES
)

fake = Faker()
Faker.seed(0)
random.seed(0)

def gen_address_row():
    return (
        fake.street_address(),
        fake.city(),
        fake.postcode(),
        fake.country()
    )

def gen_manufacturer_row(unique_set: set = None, counter: int = 0):
    base_name = fake.company()
    name = f"Man_{counter}_{base_name}"[:100]

    if unique_set is not None:
        while name in unique_set:
            unique_id = str(uuid.uuid4())[:8]
            name = f"Man_{counter}_{unique_id}_{base_name}"[:100]

        unique_set.add(name)

    return (name,)

def gen_category_row(name_hint: Optional[str] = None):
    return (f"Cat_{counter}_{name}")


def gen_attribute_row(unique_set: set = None, counter: int = 0):
    base_name = fake.word().capitalize()
    name = f"Attr_{counter}_{base_name}"[:100]

    if unique_set is not None:
        while name in unique_set:
            unique_id = str(uuid.uuid4())[:8]
            name = f"Attr_{counter}_{unique_id}_{base_name}"[:100]
        unique_set.add(name)

    return (name,)

def gen_option_row(attribute_id: int):
    return (attribute_id, fake.word())

def gen_promotion_row():
    start = fake.date_time_between(start_date='-1y', end_date='now')
    end = start + timedelta(days=random.randint(7, 180))
    discount = round(random.uniform(0.0, 50.0), 2)
    return (fake.word().capitalize(), str(discount), start.isoformat(), end.isoformat())

def gen_product_row(manufacturer_id: int):
    price = str(Decimal(random.uniform(5, 500)).quantize(Decimal('0.01')))
    name = fake.word().capitalize() + ' ' + fake.word().capitalize()
    desc = fake.sentence(nb_words=6)
    return (manufacturer_id, name, desc, price)

def gen_variant_row(product_id: int, promotion_ids: List[int], unique_skus: set = None, counter: int = 0):
    base_sku = f"VR-{counter:06d}"
    sku = f"{base_sku}-{uuid.uuid4().hex[:12]}"

    if unique_skus is not None:
        while sku in unique_skus:
            sku = f"{base_sku}-{uuid.uuid4().hex[:12]}"
        unique_skus.add(sku)

    price_modifier = str(Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')))
    promotion = random.choice(promotion_ids) if promotion_ids and random.random() < 0.12 else ''

    return (product_id, sku, price_modifier, promotion)

def gen_warehouse_row(address_id: int, unique_set: set = None, counter: int = 0):
    if counter < len(WAREHOUSE_VALUES):
        name, _ = WAREHOUSE_VALUES[counter]
        return (name, address_id)
    name, _ = WAREHOUSE_VALUES[0]
    return (name, address_id)

def gen_stockitem_row(warehouse_id, variant_id, shipment_ids=None):
    if shipment_ids and random.random() < 0.3:
        shipment_id = random.choice(shipment_ids)
    else:
        shipment_id = None
    return (shipment_id, warehouse_id, variant_id)

def gen_user_row(address_ids: List[int], unique_emails: set = None, counter: int = 0):
    fn = fake.first_name()
    ln = fake.last_name()

    if unique_emails is not None:
        email = ""
        while not email or email in unique_emails:
            unique_part = uuid.uuid4().hex[:8]
            email = f"{fn}.{ln}.{counter}.{unique_part}@example.com".lower()

        unique_emails.add(email)
    else:
        email = f"{fn}.{ln}.{counter}@example.com".lower()

    pw = fake.password(length=12)
    role = random.choice(USER_ROLES)
    address = random.choice(address_ids) if address_ids and random.random() < 0.8 else None

    return (fn, ln, email, pw, role, address)

def gen_delivery_method_row(counter: int = 0):
    if counter < len(DELIVERY_METHOD_VALUES):
        name, cost = DELIVERY_METHOD_VALUES[counter]
        return (name, cost)
    return (DELIVERY_METHOD_VALUES[0][0], DELIVERY_METHOD_VALUES[0][1])

def gen_payment_method_row(counter: int = 0):
    if counter < len(PAYMENT_METHOD_VALUES):
        return (PAYMENT_METHOD_VALUES[counter],)
    return (PAYMENT_METHOD_VALUES[0],)

def gen_status_row(counter: int = 0):
    if counter < len(STATUS_VALUES):
        return (STATUS_VALUES[counter],)
    return (STATUS_VALUES[0],)

def gen_cart_row(user_id: int):
    return (user_id,)

def gen_cartitem_row(cart_id: int, variant_id: int, quantity: int):
    return (quantity, cart_id, variant_id)

def gen_order_row(status_id: int, user_id: int, delivery_method_id: int, payment_method_id: int, billing_address_id: int, shipping_address_id: int, order_date_iso: str):
    return (status_id, user_id, delivery_method_id, payment_method_id, order_date_iso, billing_address_id, shipping_address_id)

def gen_orderitem_row(order_id: int, stock_item_id: int, unit_price: str):
    return (order_id, stock_item_id, unit_price)

def gen_shipment_row(order_id: int, unique_tracking_numbers: set | None = None, counter: int = 0):
    if unique_tracking_numbers is not None:
        while True:
            unique_id = str(uuid.uuid4()).replace('-', '')[:12]
            tracking = f"TN-{counter:08d}-{unique_id}"
            
            if tracking not in unique_tracking_numbers:
                unique_tracking_numbers.add(tracking)
                break
    else:
        tracking = fake.unique.bothify(text="TN-########")

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
    return (user_id, product_id, fake.sentence(nb_words=8), rating, posted)
