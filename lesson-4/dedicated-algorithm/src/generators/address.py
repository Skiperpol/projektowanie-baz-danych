from __future__ import annotations

from .base import fake


def gen_address_row():
    return (
        fake.street_address(),
        fake.city(),
        fake.postcode(),
        fake.country(),
    )


__all__ = ["gen_address_row"]

