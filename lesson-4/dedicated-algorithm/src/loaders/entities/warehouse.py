from __future__ import annotations

from typing import TYPE_CHECKING

from static.constants import WAREHOUSE_VALUES
from generators import gen_warehouse_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_warehouse(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    addr_ids = loader.generated_ids.get("Address", [])
    if not addr_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        for i in range(min(count, len(WAREHOUSE_VALUES))):
            name, predefined_address_id = WAREHOUSE_VALUES[i]
            if predefined_address_id <= len(addr_ids):
                aid = addr_ids[predefined_address_id - 1]
            else:
                aid = addr_ids[0] if addr_ids else None
            yield gen_warehouse_row(aid, None, i)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Warehouse"] = loader._fetch_recent_ids(
        "Warehouse", min(count, len(WAREHOUSE_VALUES))
    )


__all__ = ["load_warehouse"]

