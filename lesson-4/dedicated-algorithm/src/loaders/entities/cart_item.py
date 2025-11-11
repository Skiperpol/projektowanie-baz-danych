from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_cartitem_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_cartitem(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    cart_ids = loader.generated_ids.get("Cart", [])
    var_ids = loader.generated_ids.get("Variant", [])
    if not cart_ids or not var_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        max_attempts = 100
        for i in range(count):
            attempt = 0
            while attempt < max_attempts:
                cart = random.choice(cart_ids)
                var = random.choice(var_ids)
                pair = (cart, var)
                if pair not in loader.cartitem_pairs:
                    loader.cartitem_pairs.add(pair)
                    qty = random.randint(1, 5)
                    yield gen_cartitem_row(cart, var, qty)
                    break
                attempt += 1
            else:
                print(
                    f"  Warning: Could not generate unique (cart_id, variant_id) pair for CartItem row {i+1}"
                )
                cart = random.choice(cart_ids)
                var = random.choice(var_ids)
                pair = (cart, var)
                loader.cartitem_pairs.add(pair)
                qty = random.randint(1, 5)
                yield gen_cartitem_row(cart, var, qty)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["CartItem"] = loader._fetch_recent_ids("CartItem", count)


__all__ = ["load_cartitem"]

