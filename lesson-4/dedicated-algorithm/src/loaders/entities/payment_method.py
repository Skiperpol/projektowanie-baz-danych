from __future__ import annotations

from typing import TYPE_CHECKING

from constants import PAYMENT_METHOD_VALUES
from generators import gen_payment_method_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_payment_method(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    def rows():
        for i in range(min(count, len(PAYMENT_METHOD_VALUES))):
            yield gen_payment_method_row(i)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["PaymentMethod"] = loader._fetch_recent_ids(
        "PaymentMethod", min(count, len(PAYMENT_METHOD_VALUES))
    )


__all__ = ["load_payment_method"]

