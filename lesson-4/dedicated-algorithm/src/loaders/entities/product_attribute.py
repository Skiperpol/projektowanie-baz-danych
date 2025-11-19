from __future__ import annotations

import random
from typing import TYPE_CHECKING

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
        print(
            "  Warning: No product-category assignments available; falling back to generic ProductAttribute generation."
        )
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

    rows_generated = 0
    categories_to_process = [
        cid for cid in loader.category_order_cache if cid in loader.category_products_map
    ]

    def rows():
        nonlocal rows_generated
        
        shared_attrs_assigned = 0
        for category_id in categories_to_process:
            shared_attrs = loader.category_shared_attributes.get(category_id, [])
            if not shared_attrs:
                continue
            products = loader.category_products_map.get(category_id, [])
            if not products:
                continue
            
            for product_id in products:
                for attr_id in shared_attrs:
                    if rows_generated >= count:
                        break
                    pair = (product_id, attr_id)
                    if pair in loader.productattribute_pairs:
                        continue
                    loader.productattribute_pairs.add(pair)
                    rows_generated += 1
                    shared_attrs_assigned += 1
                    yield gen_productattribute_row(product_id, attr_id)
                
                if rows_generated >= count:
                    break
            
            if rows_generated >= count:
                break
        
        if shared_attrs_assigned > 0:
            print(f"  ✓ Faza 1 zakończona: przypisano {shared_attrs_assigned:,} wspólnych atrybutów (propagacja w dół drzewa)")
        
        optional_attrs_assigned = 0
        for category_id in categories_to_process:
            if rows_generated >= count:
                break
            
            shared_attrs = loader.category_shared_attributes.get(category_id, [])
            if not shared_attrs:
                continue
            shared_count = len(shared_attrs)
            products = loader.category_products_map.get(category_id, [])
            if not products:
                continue
            
            optional_pool = loader._get_optional_attrs_for_category(category_id, attribute_ids)
            optional_count = loader._calculate_optional_count(shared_count)
            optional_count = loader._bound_optional_count(optional_count)
            
            if optional_count <= 0:
                continue
            
            for product_id in products:
                if rows_generated >= count:
                    break
                    
                assigned_attrs = [
                    aid for aid in attribute_ids 
                    if (product_id, aid) in loader.productattribute_pairs
                ]
                
                available_optional = [aid for aid in optional_pool if aid not in assigned_attrs]
                if len(available_optional) < optional_count:
                    available_optional = [aid for aid in attribute_ids if aid not in assigned_attrs]
                if not available_optional:
                    continue
                
                sample_size = min(optional_count, len(available_optional))
                optional_attrs = random.sample(available_optional, sample_size)
                
                for attr_id in optional_attrs:
                    if rows_generated >= count:
                        break
                    pair = (product_id, attr_id)
                    if pair in loader.productattribute_pairs:
                        continue
                    loader.productattribute_pairs.add(pair)
                    rows_generated += 1
                    optional_attrs_assigned += 1
                    yield gen_productattribute_row(product_id, attr_id)
        
        if optional_attrs_assigned > 0:
            print(f"  ✓ Faza 2 zakończona: przypisano {optional_attrs_assigned:,} opcjonalnych atrybutów")
        if rows_generated < count:
            max_attempts = max(count * 20, 5000)
            attempts = 0
            while rows_generated < count and attempts < max_attempts:
                product_id = random.choice(product_ids)
                attr_id = random.choice(attribute_ids)
                pair = (product_id, attr_id)
                if pair in loader.productattribute_pairs:
                    attempts += 1
                    continue
                loader.productattribute_pairs.add(pair)
                rows_generated += 1
                yield gen_productattribute_row(product_id, attr_id)
                attempts = 0
            if rows_generated < count:
                for product_id in product_ids:
                    if rows_generated >= count:
                        break
                    for attr_id in attribute_ids:
                        if rows_generated >= count:
                            break
                        pair = (product_id, attr_id)
                        if pair in loader.productattribute_pairs:
                            continue
                        loader.productattribute_pairs.add(pair)
                        rows_generated += 1
                        yield gen_productattribute_row(product_id, attr_id)

    loader._copy_stream("public", table_name, columns, rows(), batch)
    loader.generated_ids["ProductAttribute"] = loader._fetch_recent_ids("ProductAttribute", count)


__all__ = ["load_productattribute"]

