from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_product_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_product(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    man_ids = loader.generated_ids.get("Manufacturer", [])
    if not man_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for _ in range(count):
            mid = random.choice(man_ids)
            yield gen_product_row(mid)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    prod_ids = loader._fetch_recent_ids("Product", count)
    loader.generated_ids["Product"] = prod_ids

    cur = loader.ps_conn.cursor()
    cur.execute('SELECT id, price FROM "Product" ORDER BY id DESC LIMIT %s', (count,))
    rows = cur.fetchall()
    cur.close()
    rows.reverse()
    for pid, price in rows:
        loader.product_price[pid] = str(price)


__all__ = ["load_product"]

