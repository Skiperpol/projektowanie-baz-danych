from __future__ import annotations

from typing import Optional, Tuple


def clamp_float(value: Optional[str], default: float, min_value: float, max_value: float) -> float:
    """Clamp a float value parsed from environment variable to a range."""
    if value is None:
        return max(min(default, max_value), min_value)
    try:
        parsed = float(value)
    except ValueError:
        parsed = default
    return max(min(parsed, max_value), min_value)


def parse_range(value: Optional[str], default: Tuple[int, int]) -> Tuple[int, int]:
    """Parse a range string (e.g., "2,4") into a tuple of integers."""
    if not value:
        return default
    parts = [p.strip() for p in value.split(",") if p.strip()]
    if len(parts) != 2:
        return default
    try:
        start, end = int(parts[0]), int(parts[1])
    except ValueError:
        return default
    if start > end:
        start, end = end, start
    if start < 0:
        start = 0
    return (start, end)


__all__ = ["clamp_float", "parse_range"]

