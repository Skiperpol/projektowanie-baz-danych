from __future__ import annotations

from typing import TYPE_CHECKING

from constants import STATUS_VALUES
from generators import gen_status_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_status(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    def rows():
        for i in range(min(count, len(STATUS_VALUES))):
            yield gen_status_row(i)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Status"] = loader._fetch_recent_ids(
        "Status", min(count, len(STATUS_VALUES))
    )


__all__ = ["load_status"]

