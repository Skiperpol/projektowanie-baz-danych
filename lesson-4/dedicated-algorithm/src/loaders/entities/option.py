from __future__ import annotations

import random
from typing import TYPE_CHECKING

from generators import gen_option_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_option(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    attr_ids = loader.generated_ids.get("Attribute", [])
    if not attr_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    def rows():
        max_attempts = 100
        for i in range(count):
            attempt = 0
            while attempt < max_attempts:
                aid = random.choice(attr_ids)
                _, value = gen_option_row(aid)
                pair = (aid, value)
                if pair not in loader.option_pairs:
                    loader.option_pairs.add(pair)
                    yield (aid, value)
                    break
                attempt += 1
            else:
                aid = random.choice(attr_ids)
                value = f"Option_{i}_{random.randint(1000, 9999)}"
                pair = (aid, value)
                loader.option_pairs.add(pair)
                yield (aid, value)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["Option"] = loader._fetch_recent_ids("Option", count)


__all__ = ["load_option"]

