from __future__ import annotations

from typing import TYPE_CHECKING

from constants import DELIVERY_METHOD_VALUES
from generators import gen_delivery_method_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_delivery_method(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    def rows():
        for i in range(min(count, len(DELIVERY_METHOD_VALUES))):
            yield gen_delivery_method_row(i)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["DeliveryMethod"] = loader._fetch_recent_ids(
        "DeliveryMethod", min(count, len(DELIVERY_METHOD_VALUES))
    )


__all__ = ["load_delivery_method"]

