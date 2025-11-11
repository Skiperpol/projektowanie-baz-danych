from __future__ import annotations

from typing import TYPE_CHECKING

from generators import gen_manufacturer_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_manufacturer(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    if table_name not in loader.unique_names:
        loader.unique_names[table_name] = set()
    unique_set = loader.unique_names[table_name]

    def rows():
        for _ in range(count):
            loader.unique_counter += 1
            yield gen_manufacturer_row(unique_set, loader.unique_counter)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Manufacturer"] = loader._fetch_recent_ids("Manufacturer", count)


__all__ = ["load_manufacturer"]

