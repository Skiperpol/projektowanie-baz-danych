from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_category(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    def rows():
        for i in range(count):
            name = f"Category_{i+1}"
            yield (name, None)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    category_ids = loader._fetch_recent_ids("Category", count)
    loader.generated_ids["Category"] = category_ids

    if len(category_ids) > 1:
        cur = loader.ps_conn.cursor()
        for i in range(1, len(category_ids)):
            if random.random() < 0.7:
                parent_id = random.choice(category_ids[:i])
                cur.execute(
                    'UPDATE "Category" SET parent_id = %s WHERE id = %s',
                    (parent_id, category_ids[i]),
                )
        loader.ps_conn.commit()
        cur.close()

    cur = loader.ps_conn.cursor()
    cur.execute('SELECT id, parent_id FROM "Category" ORDER BY id')
    category_rows = cur.fetchall()
    cur.close()
    loader._initialize_category_metadata(category_rows)


__all__ = ["load_category"]

