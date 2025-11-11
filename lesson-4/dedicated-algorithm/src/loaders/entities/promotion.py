from __future__ import annotations

from typing import TYPE_CHECKING

from generators import gen_promotion_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_promotion(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    def rows():
        for _ in range(count):
            yield gen_promotion_row()

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Promotion"] = loader._fetch_recent_ids("Promotion", count)


__all__ = ["load_promotion"]

