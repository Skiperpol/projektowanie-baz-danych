from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_stockitem_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_stockitem(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    var_ids = loader.generated_ids.get("Variant", [])
    wh_ids = loader.generated_ids.get("Warehouse", [])
    if not var_ids or not wh_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for _ in range(count):
            wid = random.choice(wh_ids)
            vid = random.choice(var_ids)
            yield gen_stockitem_row(wid, vid, None)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    stock_ids = loader._fetch_recent_ids("StockItem", count)
    loader.generated_ids["StockItem"] = stock_ids

    cur = loader.ps_conn.cursor()
    cur.execute('SELECT id, variant_id FROM "StockItem" ORDER BY id DESC LIMIT %s', (count,))
    rows = cur.fetchall()
    cur.close()
    rows.reverse()
    for sid, vid in rows:
        loader.stock_for_variant.setdefault(vid, []).append(sid)


__all__ = ["load_stockitem"]

