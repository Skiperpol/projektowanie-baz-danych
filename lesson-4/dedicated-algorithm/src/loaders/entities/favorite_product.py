from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_favorite_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_favoriteproduct(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    user_ids = loader.generated_ids.get("User", [])
    prod_ids = loader.generated_ids.get("Product", [])
    if not user_ids or not prod_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        max_attempts = 100
        for i in range(count):
            attempt = 0
            while attempt < max_attempts:
                u = random.choice(user_ids)
                p = random.choice(prod_ids)
                pair = (u, p)
                if pair not in loader.favoriteproduct_pairs:
                    loader.favoriteproduct_pairs.add(pair)
                    yield gen_favorite_row(u, p)
                    break
                attempt += 1
            else:
                print(
                    f"  Warning: Could not generate unique (user_id, product_id) pair for FavoriteProduct row {i+1}"
                )
                u = random.choice(user_ids)
                p = random.choice(prod_ids)
                pair = (u, p)
                loader.favoriteproduct_pairs.add(pair)
                yield gen_favorite_row(u, p)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["FavoriteProduct"] = loader._fetch_recent_ids("FavoriteProduct", count)


__all__ = ["load_favoriteproduct"]

