from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_variant_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_variant(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    prod_ids = loader.generated_ids.get("Product", [])
    promo_ids = loader.generated_ids.get("Promotion", [])
    if not prod_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for _ in range(count):
            pid = random.choice(prod_ids)
            yield gen_variant_row(pid, promo_ids, loader.unique_skus, loader.sku_counter)
            loader.sku_counter += 1

    loader._copy_stream("public", table_name, columns, rows(), batch)
    var_ids = loader._fetch_recent_ids("Variant", count)
    loader.generated_ids["Variant"] = var_ids

    cur = loader.ps_conn.cursor()
    cur.execute('SELECT id, product_id FROM "Variant" ORDER BY id DESC LIMIT %s', (count,))
    rows = cur.fetchall()
    cur.close()
    rows.reverse()
    for vid, pid in rows:
        loader.variant_to_product[vid] = pid


__all__ = ["load_variant"]

