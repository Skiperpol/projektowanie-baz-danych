from __future__ import annotations

import uuid
from typing import Optional, Set, Tuple

from .base import fake


def gen_attribute_row(unique_set: Optional[Set[str]] = None, counter: int = 0) -> Tuple[str]:
    base_name = fake.word().capitalize()
    name = f"Attr_{counter}_{base_name}"[:100]

    if unique_set is not None:
        while name in unique_set:
            unique_id = str(uuid.uuid4())[:8]
            name = f"Attr_{counter}_{unique_id}_{base_name}"[:100]
        unique_set.add(name)

    return (name,)


__all__ = ["gen_attribute_row"]

