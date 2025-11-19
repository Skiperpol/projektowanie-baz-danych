from __future__ import annotations

from typing import Optional, Sequence, Set, Tuple

from static.constants import WAREHOUSE_VALUES


def gen_warehouse_row(
    address_id: int,
    unique_set: Optional[Set[str]] = None,
    counter: int = 0,
) -> Tuple[str, int]:
    if counter < len(WAREHOUSE_VALUES):
        name, _ = WAREHOUSE_VALUES[counter]
        return (name, address_id)
    name, _ = WAREHOUSE_VALUES[0]
    return (name, address_id)


__all__ = ["gen_warehouse_row"]

