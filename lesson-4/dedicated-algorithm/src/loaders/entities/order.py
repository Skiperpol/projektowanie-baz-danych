from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_order_row
from generators.base import fake

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_order(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    user_ids = loader.generated_ids.get("User", [])
    status_ids = loader.generated_ids.get("Status", [])
    dm_ids = loader.generated_ids.get("DeliveryMethod", [])
    pm_ids = loader.generated_ids.get("PaymentMethod", [])
    addr_ids = loader.generated_ids.get("Address", [])
    if not (user_ids and status_ids and dm_ids and pm_ids and addr_ids):
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for _ in range(count):
            uid = random.choice(user_ids)
            sid = random.choice(status_ids)
            dm = random.choice(dm_ids)
            pm = random.choice(pm_ids)
            bill = random.choice(addr_ids)
            ship = random.choice(addr_ids)
            order_date = fake.date_time_between(start_date="-1y", end_date="now").isoformat()
            yield gen_order_row(sid, uid, dm, pm, bill, ship, order_date)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Order"] = loader._fetch_recent_ids("Order", count)


__all__ = ["load_order"]

