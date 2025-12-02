from __future__ import annotations

import random
from collections import defaultdict
from typing import TYPE_CHECKING

from generators import gen_productcategory_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_productcategory(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    product_ids = loader.generated_ids.get("Product", [])
    category_ids = loader.generated_ids.get("Category", [])
    if not product_ids or not category_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    loader.category_products_map = defaultdict(list)
    loader.product_to_categories = defaultdict(list)

    def rows():
        generated = 0
        shuffled_products = product_ids[:]
        random.shuffle(shuffled_products)

        if shuffled_products:
            for idx, category_id in enumerate(category_ids):
                if generated >= count:
                    break
                product_id = shuffled_products[idx % len(shuffled_products)]
                pair = (product_id, category_id)
                if pair in loader.productcategory_pairs:
                    continue
                loader._register_product_category_pair(product_id, category_id)
                generated += 1
                yield gen_productcategory_row(product_id, category_id)

        attempts = 0
        max_attempts = max(count * 10, 1000)
        while generated < count and attempts < max_attempts:
            product_id = random.choice(product_ids)
            category_id = random.choice(category_ids)
            pair = (product_id, category_id)
            if pair in loader.productcategory_pairs:
                attempts += 1
                continue
            loader._register_product_category_pair(product_id, category_id)
            generated += 1
            yield gen_productcategory_row(product_id, category_id)
            attempts = 0

        if generated < count:
            for product_id in product_ids:
                if generated >= count:
                    break
                for category_id in category_ids:
                    if generated >= count:
                        break
                    pair = (product_id, category_id)
                    if pair in loader.productcategory_pairs:
                        continue
                    loader._register_product_category_pair(product_id, category_id)
                    generated += 1
                    yield gen_productcategory_row(product_id, category_id)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["ProductCategory"] = loader._fetch_recent_ids("ProductCategory", count)


__all__ = ["load_productcategory"]

