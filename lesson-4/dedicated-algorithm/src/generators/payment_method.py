from __future__ import annotations

from typing import Tuple

from constants import PAYMENT_METHOD_VALUES


def gen_payment_method_row(counter: int = 0) -> Tuple[str]:
    if counter < len(PAYMENT_METHOD_VALUES):
        return (PAYMENT_METHOD_VALUES[counter],)
    return (PAYMENT_METHOD_VALUES[0],)


__all__ = ["gen_payment_method_row"]

