from __future__ import annotations

from typing import TYPE_CHECKING

from generators import gen_variantoption_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_variantoption(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    loader.load_simple_pair(
        "VariantOption",
        columns,
        count,
        batch,
        "Variant",
        "Option",
        gen_variantoption_row,
        loader.variantoption_pairs,
    )


__all__ = ["load_variantoption"]

