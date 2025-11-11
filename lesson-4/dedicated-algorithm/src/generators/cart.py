from __future__ import annotations

from typing import Tuple


def gen_cart_row(user_id: int) -> Tuple[int]:
    return (user_id,)


def gen_cartitem_row(cart_id: int, variant_id: int, quantity: int) -> Tuple[int, int, int]:
    return (quantity, cart_id, variant_id)


__all__ = ["gen_cart_row", "gen_cartitem_row"]

