from __future__ import annotations

import random
from typing import Optional, Sequence, Tuple


def gen_stockitem_row(
    warehouse_id: int,
    variant_id: int,
    shipment_ids: Optional[Sequence[int]] = None,
) -> Tuple[Optional[int], int, int]:
    if shipment_ids and random.random() < 0.3:
        shipment_id = random.choice(shipment_ids)
    else:
        shipment_id = None
    return (shipment_id, warehouse_id, variant_id)


__all__ = ["gen_stockitem_row"]

