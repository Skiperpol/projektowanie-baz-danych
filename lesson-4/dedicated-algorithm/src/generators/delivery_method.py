from __future__ import annotations

from typing import Tuple

from static.constants import DELIVERY_METHOD_VALUES


def gen_delivery_method_row(counter: int = 0) -> Tuple[str, str]:
    if counter < len(DELIVERY_METHOD_VALUES):
        name, cost = DELIVERY_METHOD_VALUES[counter]
        return (name, cost)
    return DELIVERY_METHOD_VALUES[0]


__all__ = ["gen_delivery_method_row"]

