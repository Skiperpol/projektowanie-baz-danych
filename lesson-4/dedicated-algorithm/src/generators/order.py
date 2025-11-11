from __future__ import annotations

from typing import Tuple


def gen_order_row(
    status_id: int,
    user_id: int,
    delivery_method_id: int,
    payment_method_id: int,
    billing_address_id: int,
    shipping_address_id: int,
    order_date_iso: str,
) -> Tuple[int, int, int, int, str, int, int]:
    return (
        status_id,
        user_id,
        delivery_method_id,
        payment_method_id,
        order_date_iso,
        billing_address_id,
        shipping_address_id,
    )


def gen_orderitem_row(order_id: int, stock_item_id: int, unit_price: str) -> Tuple[int, int, str]:
    return (order_id, stock_item_id, unit_price)


__all__ = ["gen_order_row", "gen_orderitem_row"]

