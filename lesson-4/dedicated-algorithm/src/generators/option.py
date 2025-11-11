from __future__ import annotations

from typing import Tuple

from .base import fake


def gen_option_row(attribute_id: int) -> Tuple[int, str]:
    return (attribute_id, fake.word())


__all__ = ["gen_option_row"]

