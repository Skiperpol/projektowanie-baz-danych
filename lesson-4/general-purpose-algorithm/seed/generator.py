import random
import uuid
from faker import Faker
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable

fake = Faker('pl_PL')
fake.seed_instance(42)

_email_counter = 0
_name_counter = 0
_sku_counter = 0
_tracking_counter = 0

def _generate_unique_email():
    """Generate a unique email using a counter and UUID to ensure uniqueness across batches"""
    global _email_counter
    _email_counter += 1
    unique_id = str(uuid.uuid4())[:8]
    return f"user{_email_counter}_{unique_id}@example.com"

def reset_email_counter():
    """Reset the email counter (useful when starting a new table)"""
    global _email_counter
    _email_counter = 0

def _generate_unique_name(max_chars=100, prefix=""):
    """Generate a unique name using a counter and UUID to ensure uniqueness across batches"""
    global _name_counter
    _name_counter += 1
    unique_id = str(uuid.uuid4())[:8]
    base_name = fake.company() if not prefix else f"{prefix} {fake.word()}"
    unique_name = f"{base_name} {_name_counter}_{unique_id}"
    return unique_name[:max_chars] if len(unique_name) > max_chars else unique_name

def _generate_unique_sku():
    """Generate a unique SKU using a counter and UUID to ensure uniqueness across batches"""
    global _sku_counter
    _sku_counter += 1
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"SKU-{_sku_counter:06d}-{unique_id}"

def _generate_unique_tracking():
    """Generate a unique tracking number using a counter and UUID to ensure uniqueness across batches"""
    global _tracking_counter
    _tracking_counter += 1
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"TRK-{_tracking_counter:010d}-{unique_id}"

def get_faker_for_type(column: Dict[str, Any], table_name: str) -> Optional[Callable]:
    col_name = column['name'].lower()
    data_type = str(column['data_type']).upper()
    size = column.get('size')
    constraints = [c.upper() for c in column.get("constraints", [])]
    is_unique = "UNIQUE" in constraints and col_name == "name"

    if 'email' in col_name:
        return lambda: _generate_unique_email()
    if is_unique and table_name in ["Manufacturer", "Attribute", "Warehouse", "DeliveryMethod", "PaymentMethod", "Status"]:
        max_chars = size or 100
        prefix = table_name.lower()[:3]
        return lambda: _generate_unique_name(max_chars=max_chars, prefix=prefix)
    if 'password' in col_name:
        return lambda: fake.password(length=12)
    if 'first_name' in col_name:
        return lambda: fake.first_name()
    if 'last_name' in col_name:
        return lambda: fake.last_name()
    if 'street' in col_name:
        return lambda: fake.street_address()
    if 'city' in col_name:
        return lambda: fake.city()
    if 'country' in col_name:
        max_chars = size or 255
        return lambda: fake.country()[:max_chars]
    if 'postal' in col_name:
        return lambda: fake.postcode()
    if 'sku' in col_name:
        return lambda: _generate_unique_sku()
    if 'tracking' in col_name:
        def generate_tracking():
            if fake.boolean(chance_of_getting_true=80):
                return _generate_unique_tracking()
            return None
        return generate_tracking
    if col_name == 'role':
        return lambda: random.choice(['user', 'admin', 'warehouseman', 'editor'])
    if 'description' in col_name:
        return lambda: fake.text(max_nb_chars=size or 300)

    if 'INTEGER' in data_type or data_type == 'INT':
        if 'quantity' in col_name:
            return lambda: random.randint(1, 10)
        if 'rating' in col_name:
            return lambda: random.randint(1, 5)
        return lambda: random.randint(1, 10000)
    if 'VARCHAR' in data_type or 'TEXT' in data_type or data_type == 'CHAR':
        max_chars = size or 255
        if max_chars <= 20:
            return lambda: (fake.word() or '')[:max_chars]
        elif max_chars <= 50:
            return lambda: (fake.sentence(nb_words=3) or '')[:max_chars]
        else:
            def generate_text():
                text = fake.text(max_nb_chars=max_chars + 100)
                text = ' '.join(text.split())[:max_chars]
                return text
            return generate_text
    if 'DECIMAL' in data_type or 'NUMERIC' in data_type:
        if 'price' in col_name or 'cost' in col_name:
            return lambda: Decimal(str(round(random.uniform(1.0, 1000.0), 2)))
        if 'discount' in col_name:
            return lambda: Decimal(str(round(random.uniform(0, 50), 2)))
        return lambda: Decimal(str(round(random.uniform(0, 10000), 2)))
    if 'TIMESTAMP' in data_type or 'TIMESTAMPTZ' in data_type:
        return lambda: fake.date_time_between(start_date='-2y', end_date='now')
    return lambda: fake.word()
