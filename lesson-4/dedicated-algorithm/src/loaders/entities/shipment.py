from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_shipment_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_shipment(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    order_ids = loader.generated_ids.get("Order", [])
    if not order_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for _ in range(count):
            oid = random.choice(order_ids)
            yield gen_shipment_row(oid, loader.unique_tracking_numbers, loader.tracking_counter)
            loader.tracking_counter += 1

    loader._copy_stream("public", table_name, columns, rows(), batch)
    shipment_ids = loader._fetch_recent_ids("Shipment", count)
    loader.generated_ids["Shipment"] = shipment_ids

    stock_ids = loader.generated_ids.get("StockItem", [])
    if stock_ids and shipment_ids:
        cur = loader.ps_conn.cursor()
        for stock_id in stock_ids:
            if random.random() < 0.3:
                shipment_id = random.choice(shipment_ids)
                cur.execute(
                    'UPDATE "StockItem" SET shipment_id = %s WHERE id = %s',
                    (shipment_id, stock_id),
                )
        loader.ps_conn.commit()
        cur.close()


__all__ = ["load_shipment"]

