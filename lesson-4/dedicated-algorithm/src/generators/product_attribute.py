from __future__ import annotations

from typing import Tuple


def gen_productattribute_row(product_id: int, attribute_id: int) -> Tuple[int, int]:
    return (product_id, attribute_id)


__all__ = ["gen_productattribute_row"]

