from __future__ import annotations

import random
import uuid
from decimal import Decimal
from typing import List, Optional, Sequence, Set, Tuple


def gen_variant_row(
    product_id: int,
    promotion_ids: Sequence[int],
    unique_skus: Optional[Set[str]] = None,
    counter: int = 0,
) -> Tuple[int, str, str, Optional[int]]:
    base_sku = f"VR-{counter:06d}"
    sku = f"{base_sku}-{uuid.uuid4().hex[:12]}"

    if unique_skus is not None:
        while sku in unique_skus:
            sku = f"{base_sku}-{uuid.uuid4().hex[:12]}"
        unique_skus.add(sku)

    price_modifier = str(Decimal(random.uniform(0, 100)).quantize(Decimal("0.01")))
    promotion = random.choice(promotion_ids) if promotion_ids and random.random() < 0.12 else ""

    return (product_id, sku, price_modifier, promotion)


__all__ = ["gen_variant_row"]

