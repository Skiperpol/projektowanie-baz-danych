from typing import Dict, List, Tuple


class ValidationError(Exception):
    """Configuration validation error."""
    pass


class RowCountsValidator:
    """Validator checking consistency of row_counts.json."""

    def __init__(self, row_counts: Dict[str, int]):
        self.row_counts = row_counts
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """
        Performs all validations.
        Returns: (is_valid, errors, warnings)
        """
        self.errors.clear()
        self.warnings.clear()

        self._validate_basic_requirements()
        self._validate_foreign_key_relationships()
        self._validate_unique_pair_constraints()
        self._validate_category_attribute_propagation()
        self._validate_reasonable_ratios()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def _validate_basic_requirements(self):
        """Basic requirements - non-negative values, reasonable numbers."""
        for table, count in self.row_counts.items():
            if count < 0:
                self.errors.append(f"{table}: Liczba nie może być ujemna (obecnie: {count})")

    def _validate_foreign_key_relationships(self):
        """Validation of foreign key relationships - whether there are sufficient sources."""
        if self.row_counts.get("Cart", 0) > self.row_counts.get("User", 0):
            self.warnings.append(
                f"Cart ({self.row_counts.get('Cart', 0)}) > User ({self.row_counts.get('User', 0)}) - "
                "niektórzy użytkownicy będą mieli wiele koszyków"
            )

        if self.row_counts.get("Variant", 0) < self.row_counts.get("Product", 0):
            self.warnings.append(
                f"Variant ({self.row_counts.get('Variant', 0)}) < Product ({self.row_counts.get('Product', 0)}) - "
                "niektóre produkty mogą nie mieć wariantów"
            )

        if self.row_counts.get("StockItem", 0) < self.row_counts.get("Variant", 0):
            self.warnings.append(
                f"StockItem ({self.row_counts.get('StockItem', 0)}) < Variant ({self.row_counts.get('Variant', 0)}) - "
                "niektóre warianty mogą nie mieć stanu magazynowego"
            )

        if self.row_counts.get("Address", 0) < self.row_counts.get("User", 0):
            self.warnings.append(
                f"Address ({self.row_counts.get('Address', 0)}) < User ({self.row_counts.get('User', 0)}) - "
                "niektórzy użytkownicy mogą nie mieć adresu"
            )

    def _validate_unique_pair_constraints(self):
        """Validation of unique pair constraints."""
        max_orderitem = self.row_counts.get("Order", 0) * self.row_counts.get("StockItem", 0)
        requested_orderitem = self.row_counts.get("OrderItem", 0)
        if requested_orderitem > max_orderitem:
            self.errors.append(
                f"OrderItem ({requested_orderitem}) > max możliwych ({max_orderitem}) = "
                f"Order ({self.row_counts.get('Order', 0)}) * StockItem ({self.row_counts.get('StockItem', 0)})"
            )
        elif requested_orderitem > max_orderitem * 0.5:
            self.warnings.append(
                f"OrderItem ({requested_orderitem}) > 50% max możliwych ({max_orderitem}) - "
                "może być trudno wygenerować unikalne pary"
            )

        max_cartitem = self.row_counts.get("Cart", 0) * self.row_counts.get("Variant", 0)
        requested_cartitem = self.row_counts.get("CartItem", 0)
        if requested_cartitem > max_cartitem:
            self.errors.append(
                f"CartItem ({requested_cartitem}) > max możliwych ({max_cartitem}) = "
                f"Cart ({self.row_counts.get('Cart', 0)}) * Variant ({self.row_counts.get('Variant', 0)})"
            )

        max_favorite = self.row_counts.get("User", 0) * self.row_counts.get("Product", 0)
        requested_favorite = self.row_counts.get("FavoriteProduct", 0)
        if requested_favorite > max_favorite:
            self.errors.append(
                f"FavoriteProduct ({requested_favorite}) > max możliwych ({max_favorite}) = "
                f"User ({self.row_counts.get('User', 0)}) * Product ({self.row_counts.get('Product', 0)})"
            )

        max_review = self.row_counts.get("User", 0) * self.row_counts.get("Product", 0)
        requested_review = self.row_counts.get("Review", 0)
        if requested_review > max_review:
            self.errors.append(
                f"Review ({requested_review}) > max możliwych ({max_review}) = "
                f"User ({self.row_counts.get('User', 0)}) * Product ({self.row_counts.get('Product', 0)})"
            )

        max_productcategory = self.row_counts.get("Product", 0) * self.row_counts.get("Category", 0)
        requested_productcategory = self.row_counts.get("ProductCategory", 0)
        if requested_productcategory > max_productcategory:
            self.errors.append(
                f"ProductCategory ({requested_productcategory}) > max możliwych ({max_productcategory}) = "
                f"Product ({self.row_counts.get('Product', 0)}) * Category ({self.row_counts.get('Category', 0)})"
            )

        max_productattribute = self.row_counts.get("Product", 0) * self.row_counts.get("Attribute", 0)
        requested_productattribute = self.row_counts.get("ProductAttribute", 0)
        if requested_productattribute > max_productattribute:
            self.errors.append(
                f"ProductAttribute ({requested_productattribute}) > max możliwych ({max_productattribute}) = "
                f"Product ({self.row_counts.get('Product', 0)}) * Attribute ({self.row_counts.get('Attribute', 0)})"
            )

        max_variantoption = self.row_counts.get("Variant", 0) * self.row_counts.get("Option", 0)
        requested_variantoption = self.row_counts.get("VariantOption", 0)
        if requested_variantoption > max_variantoption:
            self.errors.append(
                f"VariantOption ({requested_variantoption}) > max możliwych ({max_variantoption}) = "
                f"Variant ({self.row_counts.get('Variant', 0)}) * Option ({self.row_counts.get('Option', 0)})"
            )

    def _validate_category_attribute_propagation(self):
        """
        Validation of requirements for attribute propagation in categories.
        Products in subcategories should have all common attributes from the parent category.
        """
        product_count = self.row_counts.get("Product", 0)
        attribute_count = self.row_counts.get("Attribute", 0)
        productattribute_count = self.row_counts.get("ProductAttribute", 0)
        category_count = self.row_counts.get("Category", 0)

        if product_count == 0 or attribute_count == 0:
            return

        min_attributes_per_product = 3
        max_attributes_per_product = max(attribute_count, 10)

        min_required = product_count * min_attributes_per_product
        max_reasonable = product_count * max_attributes_per_product

        if productattribute_count < min_required:
            self.errors.append(
                f"ProductAttribute ({productattribute_count}) < minimalne wymagane ({min_required}) = "
                f"Product ({product_count}) * {min_attributes_per_product} (min atrybutów na produkt). "
                "Produkty w podkategoriach mogą nie otrzymać wszystkich dziedziczonych atrybutów."
            )
        elif productattribute_count < min_required * 1.5:
            self.warnings.append(
                f"ProductAttribute ({productattribute_count}) może być niewystarczające dla pełnej propagacji. "
                f"Zalecane: >= {int(min_required * 1.5)} (dla {product_count} produktów)"
            )

        if category_count > 0 and attribute_count < category_count:
            self.warnings.append(
                f"Attribute ({attribute_count}) < Category ({category_count}) - "
                "niektóre kategorie mogą mieć bardzo mało atrybutów"
            )
        if max_reasonable < productattribute_count:
            self.warnings.append(
                f"ProductAttribute ({productattribute_count}) > max możliwych ({max_reasonable}) = "
                f"Product ({product_count}) * {max_attributes_per_product} (max atrybutów na produkt). "
                "Produkty w podkategoriach mogą otrzymać więcej atrybutów niż jest dostępnych"
            )

    def _validate_reasonable_ratios(self):
        """Validation of reasonable ratios between tables."""
        option_count = self.row_counts.get("Option", 0)
        attribute_count = self.row_counts.get("Attribute", 0)
        if attribute_count > 0:
            avg_options_per_attribute = option_count / attribute_count
            if avg_options_per_attribute < 10:
                self.warnings.append(
                    f"Option ({option_count}) / Attribute ({attribute_count}) = {avg_options_per_attribute:.1f} - "
                    "średnio < 10 opcji na atrybut, może być trudno wygenerować unikalne pary"
                )
            elif avg_options_per_attribute > 200:
                self.warnings.append(
                    f"Option ({option_count}) / Attribute ({attribute_count}) = {avg_options_per_attribute:.1f} - "
                    "bardzo dużo opcji na atrybut (>200)"
                )

        productattribute_count = self.row_counts.get("ProductAttribute", 0)
        product_count = self.row_counts.get("Product", 0)
        if product_count > 0:
            avg_attributes_per_product = productattribute_count / product_count
            if avg_attributes_per_product < 1:
                self.warnings.append(
                    f"ProductAttribute ({productattribute_count}) / Product ({product_count}) = {avg_attributes_per_product:.2f} - "
                    "średnio < 1 atrybutu na produkt"
                )
            elif avg_attributes_per_product > 20:
                self.warnings.append(
                    f"ProductAttribute ({productattribute_count}) / Product ({product_count}) = {avg_attributes_per_product:.2f} - "
                    "bardzo dużo atrybutów na produkt (>20)"
                )

        variantoption_count = self.row_counts.get("VariantOption", 0)
        variant_count = self.row_counts.get("Variant", 0)
        if variant_count > 0:
            avg_options_per_variant = variantoption_count / variant_count
            if avg_options_per_variant < 0.5:
                self.warnings.append(
                    f"VariantOption ({variantoption_count}) / Variant ({variant_count}) = {avg_options_per_variant:.2f} - "
                    "średnio < 0.5 opcji na wariant"
                )
            elif avg_options_per_variant > 10:
                self.warnings.append(
                    f"VariantOption ({variantoption_count}) / Variant ({variant_count}) = {avg_options_per_variant:.2f} - "
                    "bardzo dużo opcji na wariant (>10)"
                )

        productcategory_count = self.row_counts.get("ProductCategory", 0)
        product_count = self.row_counts.get("Product", 0)
        if product_count > 0:
            avg_categories_per_product = productcategory_count / product_count
            if avg_categories_per_product < 0.5:
                self.warnings.append(
                    f"ProductCategory ({productcategory_count}) / Product ({product_count}) = {avg_categories_per_product:.2f} - "
                    "średnio < 0.5 kategorii na produkt"
                )
            elif avg_categories_per_product > 5:
                self.warnings.append(
                    f"ProductCategory ({productcategory_count}) / Product ({product_count}) = {avg_categories_per_product:.2f} - "
                    "bardzo dużo kategorii na produkt (>5)"
                )


def validate_row_counts(row_counts: Dict[str, int]) -> Tuple[bool, List[str], List[str]]:
    validator = RowCountsValidator(row_counts)
    return validator.validate_all()


__all__ = ["validate_row_counts", "RowCountsValidator", "ValidationError"]

