from __future__ import annotations

import random
import uuid
from typing import Optional, Sequence, Set, Tuple

from static.constants import USER_ROLES
from .base import fake


def gen_user_row(
    address_ids: Sequence[int],
    unique_emails: Optional[Set[str]] = None,
    counter: int = 0,
) -> Tuple[str, str, str, str, str, Optional[int]]:
    fn = fake.first_name()
    ln = fake.last_name()

    if unique_emails is not None:
        email = ""
        while not email or email in unique_emails:
            unique_part = uuid.uuid4().hex[:8]
            email = f"{fn}.{ln}.{counter}.{unique_part}@example.com".lower()

        unique_emails.add(email)
    else:
        email = f"{fn}.{ln}.{counter}@example.com".lower()

    pw = fake.password(length=12)
    role = random.choice(USER_ROLES)
    address = random.choice(address_ids) if address_ids and random.random() < 0.8 else None

    return (fn, ln, email, pw, role, address)


__all__ = ["gen_user_row"]

