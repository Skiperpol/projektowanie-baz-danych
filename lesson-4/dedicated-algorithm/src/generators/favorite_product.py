from __future__ import annotations

from typing import Tuple


def gen_favorite_row(user_id: int, product_id: int) -> Tuple[int, int]:
    return (user_id, product_id)


__all__ = ["gen_favorite_row"]

