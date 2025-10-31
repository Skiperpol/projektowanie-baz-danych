from datetime import timedelta
from decimal import Decimal
import random
from typing import Dict, List, Any, Optional

def variant_price_from_product(product_price: Decimal, modifier: Decimal) -> Decimal:
    return (product_price + modifier).quantize(Decimal("0.01"))

def promotion_dates(start):
    return start, start + timedelta(days=random.randint(1, 90))

def shipment_date_for_order(order_date):
    return order_date + timedelta(days=random.randint(0, 14))

def posted_at_after_shipment(shipped_at):
    return shipped_at + timedelta(days=random.randint(0, 30))
