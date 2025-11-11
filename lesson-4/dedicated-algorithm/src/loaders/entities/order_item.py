from __future__ import annotations

import random
from decimal import Decimal
from typing import TYPE_CHECKING

from generators import gen_orderitem_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_orderitem(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    order_ids = loader.generated_ids.get("Order", [])
    stock_ids = loader.generated_ids.get("StockItem", [])
    if not order_ids or not stock_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    possible_pairs = len(order_ids) * len(stock_ids)

    if count > possible_pairs:
        raise ValueError(
            f"Too many OrderItem rows requested ({count}), max unique combinations: {possible_pairs}"
        )

    pairs = set()
    while len(pairs) < count:
        pairs.add((random.choice(order_ids), random.choice(stock_ids)))

    def rows():
        for oid, sid in pairs:
            unit_price = str(Decimal(random.uniform(5, 500)).quantize(Decimal("0.01")))
            yield gen_orderitem_row(oid, sid, unit_price)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["OrderItem"] = loader._fetch_recent_ids("OrderItem", count)


__all__ = ["load_orderitem"]

