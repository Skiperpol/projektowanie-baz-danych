from __future__ import annotations

import random
from typing import TYPE_CHECKING
from itertools import chain

from generators import gen_productattribute_row

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader


def load_productattribute(loader: "StreamLoader", table_name: str, columns, count: int, batch: int):
    attribute_ids = loader.generated_ids.get("Attribute", [])
    product_ids = loader.generated_ids.get("Product", [])

    if not attribute_ids or not product_ids:
        loader._load_generic(table_name, columns, count, batch)
        return

    if not loader.category_parent:
        loader._ensure_category_metadata()

    if not loader.category_products_map:
        print("  Warning: No product-category assignments; falling back to generic generation.")
        loader.load_simple_pair(
            "ProductAttribute",
            columns,
            count,
            batch,
            "Product",
            "Attribute",
            gen_productattribute_row,
            loader.productattribute_pairs,
        )
        return

    loader._build_category_shared_attributes(attribute_ids)

    categories = [
        cid for cid in loader.category_order_cache
        if cid in loader.category_products_map
    ]

    def gen_shared():
        assigned = 0
        for cat in categories:
            shared_attrs = loader.category_shared_attributes.get(cat, [])
            products = loader.category_products_map.get(cat, [])
            if not shared_attrs or not products:
                continue

            for product_id in products:
                for attr_id in shared_attrs:
                    pair = (product_id, attr_id)
                    if pair in loader.productattribute_pairs:
                        continue
                    loader.productattribute_pairs.add(pair)
                    assigned += 1
                    yield gen_productattribute_row(product_id, attr_id)

        if assigned:
            print(f"  ✓ Faza 1: przypisano {assigned:,} wspólnych atrybutów")
    
    def gen_optional():
        assigned = 0

        for cat in categories:
            shared_attrs = loader.category_shared_attributes.get(cat, [])
            products = loader.category_products_map.get(cat, [])
            if not shared_attrs or not products:
                continue

            optional_pool = loader._get_optional_attrs_for_category(cat, attribute_ids)
            optional_count = loader._bound_optional_count(
                loader._calculate_optional_count(len(shared_attrs))
            )
            if optional_count <= 0:
                continue

            for product_id in products:
                existing = {
                    aid for _, aid in loader.productattribute_pairs
                    if product_id == _
                }

                available = [a for a in optional_pool if a not in existing]
                if len(available) < optional_count:
                    available = [a for a in attribute_ids if a not in existing]
                if not available:
                    continue

                chosen = random.sample(available, min(optional_count, len(available)))

                for attr_id in chosen:
                    pair = (product_id, attr_id)
                    if pair in loader.productattribute_pairs:
                        continue
                    loader.productattribute_pairs.add(pair)
                    assigned += 1
                    yield gen_productattribute_row(product_id, attr_id)

        if assigned:
            print(f"  ✓ Faza 2: przypisano {assigned:,} opcjonalnych atrybutów")
    
    def gen_fill_remaining():
        needed = count - len(loader.productattribute_pairs)
        if needed <= 0:
            return

        attempts = 0
        max_attempts = max(count * 20, 5000)

        while len(loader.productattribute_pairs) < count and attempts < max_attempts:
            pair = (random.choice(product_ids), random.choice(attribute_ids))
            if pair in loader.productattribute_pairs:
                attempts += 1
                continue
            loader.productattribute_pairs.add(pair)
            yield gen_productattribute_row(*pair)
            attempts = 0

        if len(loader.productattribute_pairs) < count:
            for p in product_ids:
                for a in attribute_ids:
                    if len(loader.productattribute_pairs) >= count:
                        return
                    pair = (p, a)
                    if pair in loader.productattribute_pairs:
                        continue
                    loader.productattribute_pairs.add(pair)
                    yield gen_productattribute_row(p, a)

    all_rows = chain(gen_shared(), gen_optional(), gen_fill_remaining())

    loader._copy_stream("public", table_name, columns, all_rows, batch)
    loader.generated_ids["ProductAttribute"] = loader._fetch_recent_ids("ProductAttribute", count)


__all__ = ["load_productattribute"]
