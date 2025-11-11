from __future__ import annotations

from typing import Tuple

from constants import STATUS_VALUES


def gen_status_row(counter: int = 0) -> Tuple[str]:
    if counter < len(STATUS_VALUES):
        return (STATUS_VALUES[counter],)
    return (STATUS_VALUES[0],)


__all__ = ["gen_status_row"]

