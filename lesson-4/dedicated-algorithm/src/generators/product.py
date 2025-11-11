from __future__ import annotations

import random
from decimal import Decimal
from typing import Tuple

from .base import fake


def gen_product_row(manufacturer_id: int) -> Tuple[int, str, str, str]:
    price = str(Decimal(random.uniform(5, 500)).quantize(Decimal("0.01")))
    name = fake.word().capitalize() + " " + fake.word().capitalize()
    desc = fake.sentence(nb_words=6)
    return (manufacturer_id, name, desc, price)


__all__ = ["gen_product_row"]

