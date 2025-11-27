from __future__ import annotations

import os
import random
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from loaders.stream_loader import StreamLoader

from ..utils import clamp_float, parse_range


class CategoryHelper:
    """Helper class for category-related operations."""

    def __init__(self, loader: "StreamLoader"):
        self.loader = loader
        self.common_attribute_ratio = clamp_float(
            os.getenv("COMMON_ATTRIBUTE_RATIO"), 0.8, 0.1, 0.95
        )
        self.common_attribute_variation = clamp_float(
            os.getenv("COMMON_ATTRIBUTE_VARIATION"), 0.05, 0.0, 0.2
        )
        self.root_shared_attr_range = parse_range(
            os.getenv("ROOT_SHARED_ATTRIBUTE_RANGE"), (2, 4)
        )
        self.child_additional_attr_range = parse_range(
            os.getenv("CHILD_ADDITIONAL_ATTRIBUTE_RANGE"), (1, 2)
        )
        self.product_optional_attr_range = parse_range(
            os.getenv("PRODUCT_OPTIONAL_ATTRIBUTE_RANGE"), (0, 10)
        )
        self.optional_pool_size = max(0, int(os.getenv("CATEGORY_OPTIONAL_POOL_SIZE", "8")))

    def ensure_category_metadata(self):
        """Ensure category metadata is loaded from database."""
        if self.loader.category_parent:
            return
        cur = self.loader.ps_conn.cursor()
        cur.execute('SELECT id, parent_id FROM "Category"')
        rows = cur.fetchall()
        cur.close()
        self.initialize_category_metadata(rows)

    def initialize_category_metadata(self, category_rows: List[Tuple[int, Optional[int]]]):
        """Initialize category metadata structures from database rows."""
        self.loader.category_parent = {}
        self.loader.category_children = defaultdict(list)
        for cid, parent_id in category_rows:
            self.loader.category_parent[cid] = parent_id
            if parent_id is not None:
                self.loader.category_children[parent_id].append(cid)
        self.loader.category_depth = {}
        for cid in self.loader.category_parent:
            self.compute_category_depth(cid)
        self.loader.category_order_cache = sorted(
            self.loader.category_parent.keys(), key=lambda c: self.loader.category_depth.get(c, 0)
        )
        self.loader.category_shared_attributes = {}
        self.loader.category_optional_pool = {}

    def compute_category_depth(self, category_id: int) -> int:
        """Compute and cache the depth of a category in the hierarchy."""
        if category_id in self.loader.category_depth:
            return self.loader.category_depth[category_id]
        parent_id = self.loader.category_parent.get(category_id)
        if parent_id is None:
            depth = 0
        else:
            depth = 1 + self.compute_category_depth(parent_id)
        self.loader.category_depth[category_id] = depth
        return depth

    def build_category_shared_attributes(self, attribute_ids: List[int]):
        """Build shared attributes for each category based on hierarchy."""
        if self.loader.category_shared_attributes or not attribute_ids:
            return
        if not self.loader.category_parent:
            self.ensure_category_metadata()

        for category_id in self.loader.category_order_cache:
            parent_id = self.loader.category_parent.get(category_id)
            parent_shared_list = self._get_parent_attributes(parent_id)
            parent_attrs = set(parent_shared_list)
            extra_attribute_count = self._compute_extra_attribute_count(parent_id)
            extra_attrs = self._pick_extra_attributes(attribute_ids, parent_attrs, extra_attribute_count)

            combined = list(dict.fromkeys(parent_shared_list + extra_attrs))
            if not combined and attribute_ids:
                combined = [random.choice(attribute_ids)]

            self.loader.category_shared_attributes[category_id] = combined

    def get_optional_attrs_for_category(self, category_id: int, attribute_ids: List[int]) -> List[int]:
        """Get optional attributes pool for a category."""
        if category_id not in self.loader.category_optional_pool:
            candidates = self._filter_shared_attributes(category_id, attribute_ids)
            candidates = self._ensure_min_candidates(candidates, attribute_ids)
            pool = self._pick_optional_attributes(candidates)
            self.loader.category_optional_pool[category_id] = pool
        return self.loader.category_optional_pool[category_id]

    def calculate_optional_count(self, shared_count: int) -> int:
        """Calculate the number of optional attributes based on shared count."""
        if shared_count == 0:
            return 0
        ratio = random.uniform(
            max(self.common_attribute_ratio - self.common_attribute_variation, 0.05),
            min(self.common_attribute_ratio + self.common_attribute_variation, 0.95)
        )
        optional = round(shared_count * (1 - ratio) / ratio)
        return max(optional, 0)

    def bound_optional_count(self, optional_count: int) -> int:
        """Bound optional count to configured range."""
        min_val, max_val = self.product_optional_attr_range
        optional_count = max(optional_count, min_val)
        optional_count = min(optional_count, max_val)
        return optional_count

    def register_product_category_pair(self, product_id: int, category_id: int):
        """Register a product-category pair."""
        pair = (product_id, category_id)
        self.loader.productcategory_pairs.add(pair)
        self.loader.category_products_map[category_id].append(product_id)
        self.loader.product_to_categories[product_id].append(category_id)

    def _get_parent_attributes(self, parent_id: Optional[int]) -> List[int]:
        """Return shared attributes of the parent category (empty list if no parent)."""
        return self.loader.category_shared_attributes.get(parent_id, [])

    def _compute_extra_attribute_count(self, parent_id: Optional[int]) -> int:
        """Compute how many extra attributes to assign based on parent."""
        range_to_use = self.root_shared_attr_range if parent_id is None else self.child_additional_attr_range
        min_extra, max_extra = range_to_use
        return random.randint(min_extra, max_extra) if max_extra > 0 else 0

    def _pick_extra_attributes(self, attribute_ids: List[int], parent_attrs: set, extra_count: int) -> List[int]:
        """Select extra attributes that are not already in parent's shared attributes."""
        available = [aid for aid in attribute_ids if aid not in parent_attrs]
        if len(available) < extra_count:
            available = attribute_ids[:]
        return random.sample(available, extra_count) if extra_count > 0 and available else []

    def _filter_shared_attributes(self, category_id: int, attribute_ids: List[int]) -> List[int]:
        """Return attributes that are not shared for the category."""
        shared = set(self.loader.category_shared_attributes.get(category_id, []))
        return [aid for aid in attribute_ids if aid not in shared]

    def _ensure_min_candidates(self, candidates: List[int], all_attributes: List[int]) -> List[int]:
        """Ensure there are enough candidates; fallback to all attributes if needed."""
        if len(candidates) < self.optional_pool_size:
            return all_attributes[:]
        return candidates

    def _pick_optional_attributes(self, candidates: List[int]) -> List[int]:
        """Pick random attributes from candidates, limited by optional_pool_size."""
        if self.optional_pool_size == 0 or not candidates:
            return []
        unique_candidates = list(dict.fromkeys(candidates))
        sample_size = min(self.optional_pool_size, len(unique_candidates))
        return random.sample(unique_candidates, sample_size)

__all__ = ["CategoryHelper"]

