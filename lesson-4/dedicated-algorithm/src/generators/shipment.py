from __future__ import annotations

import random
import uuid
from typing import Optional, Sequence, Set, Tuple

from .base import fake


def gen_shipment_row(
    order_id: int,
    unique_tracking_numbers: Optional[Set[str]] = None,
    counter: int = 0,
) -> Tuple[int, str, str]:
    if unique_tracking_numbers is not None:
        while True:
            unique_id = str(uuid.uuid4()).replace("-", "")[:12]
            tracking = f"TN-{counter:08d}-{unique_id}"
            if tracking not in unique_tracking_numbers:
                unique_tracking_numbers.add(tracking)
                break
    else:
        tracking = fake.unique.bothify(text="TN-########")

    shipped_at = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
    return (order_id, tracking, shipped_at)


__all__ = ["gen_shipment_row"]

