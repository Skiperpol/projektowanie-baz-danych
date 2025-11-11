from __future__ import annotations

from typing import Optional, Tuple

from .base import fake


def gen_category_row(name_hint: Optional[str] = None, parent_id: Optional[int] = None) -> Tuple[str, Optional[int]]:
    name = name_hint or fake.word().capitalize()
    return (name, parent_id)


__all__ = ["gen_category_row"]

