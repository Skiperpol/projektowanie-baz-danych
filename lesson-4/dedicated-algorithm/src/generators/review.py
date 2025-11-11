from __future__ import annotations

import random
from typing import Tuple

from .base import fake


def gen_review_row(user_id: int, product_id: int) -> Tuple[int, int, str, int, str]:
    rating = random.randint(1, 5)
    posted = fake.date_time_between(start_date="-2y", end_date="now").isoformat()
    return (user_id, product_id, fake.sentence(nb_words=8), rating, posted)


__all__ = ["gen_review_row"]

