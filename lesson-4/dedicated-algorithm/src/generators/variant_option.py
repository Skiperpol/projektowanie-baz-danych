from __future__ import annotations

from typing import Tuple


def gen_variantoption_row(variant_id: int, option_id: int) -> Tuple[int, int]:
    return (variant_id, option_id)


__all__ = ["gen_variantoption_row"]

