from __future__ import annotations

from typing import Tuple


def gen_productcategory_row(product_id: int, category_id: int) -> Tuple[int, int]:
    return (product_id, category_id)


__all__ = ["gen_productcategory_row"]

