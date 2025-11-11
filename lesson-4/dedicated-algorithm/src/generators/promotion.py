from __future__ import annotations

import random
from datetime import timedelta
from typing import Tuple

from .base import fake


def gen_promotion_row() -> Tuple[str, str, str, str]:
    start = fake.date_time_between(start_date="-1y", end_date="now")
    end = start + timedelta(days=random.randint(7, 180))
    discount = round(random.uniform(0.0, 50.0), 2)
    return (fake.word().capitalize(), str(discount), start.isoformat(), end.isoformat())


__all__ = ["gen_promotion_row"]

