from __future__ import annotations

from typing import TYPE_CHECKING

from generators import gen_user_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_user(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    addr_ids = loader.generated_ids.get("Address", [])

    def rows():
        for _ in range(count):
            yield gen_user_row(addr_ids, loader.unique_emails, loader.email_counter)
            loader.email_counter += 1

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["User"] = loader._fetch_recent_ids("User", count)


__all__ = ["load_user"]

