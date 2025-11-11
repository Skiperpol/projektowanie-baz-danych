from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_cart_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_cart(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    user_ids = loader.generated_ids.get("User", [])
    if not user_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    chosen = random.sample(user_ids, min(count, len(user_ids)))

    def rows():
        for uid in chosen:
            yield gen_cart_row(uid)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    cart_ids = loader._fetch_recent_ids("Cart", len(chosen))
    loader.generated_ids["Cart"] = cart_ids
    for user_id, cart_id in zip(chosen, cart_ids):
        loader.generated_ids.setdefault("user_to_cart_map", {})
        loader.generated_ids["user_to_cart_map"][user_id] = cart_id


__all__ = ["load_cart"]

