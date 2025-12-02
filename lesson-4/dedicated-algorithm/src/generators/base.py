from __future__ import annotations

import random
from faker import Faker

fake = Faker()
Faker.seed(0)
random.seed(0)

__all__ = ["fake"]

