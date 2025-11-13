import json
from pathlib import Path
from validators import validate_row_counts


def suggest_row_counts(current_counts: dict) -> dict:
    suggested = current_counts.copy()
    
    product_count = current_counts.get("Product", 0)
    attribute_count = current_counts.get("Attribute", 0)
    category_count = current_counts.get("Category", 0)
    
    if product_count > 0:
        min_attrs_per_product = 3
        recommended_attrs_per_product = 5
        current_productattribute = current_counts.get("ProductAttribute", 0)
        min_required = product_count * min_attrs_per_product
        recommended = product_count * recommended_attrs_per_product
        
        if current_productattribute < min_required:
            suggested["ProductAttribute"] = int(recommended * 1.2)
            print(f"  ProductAttribute: {current_productattribute} -> {suggested['ProductAttribute']} "
                  f"(min: {min_required}, zalecane: {recommended})")
    
    if attribute_count > 0:
        current_option = current_counts.get("Option", 0)
        min_options_per_attr = 50
        recommended_options_per_attr = 80
        min_required = attribute_count * min_options_per_attr
        recommended = attribute_count * recommended_options_per_attr
        
        if current_option < min_required:
            suggested["Option"] = int(recommended * 1.1)
            print(f"  Option: {current_option} -> {suggested['Option']} "
                  f"(min: {min_required}, zalecane: {recommended})")
    
    variant_count = current_counts.get("Variant", 0)
    if variant_count > 0:
        current_variantoption = current_counts.get("VariantOption", 0)
        recommended_options_per_variant = 2.5
        recommended = int(variant_count * recommended_options_per_variant)
        
        if current_variantoption < recommended * 0.8:
            suggested["VariantOption"] = int(recommended * 1.1)
            print(f"  VariantOption: {current_variantoption} -> {suggested['VariantOption']} "
                  f"(zalecane: {recommended})")
    
    if product_count > 0:
        current_productcategory = current_counts.get("ProductCategory", 0)
        recommended_categories_per_product = 1.2
        recommended = int(product_count * recommended_categories_per_product)
        
        if current_productcategory < recommended * 0.8:
            suggested["ProductCategory"] = int(recommended * 1.1)
            print(f"  ProductCategory: {current_productcategory} -> {suggested['ProductCategory']} "
                  f"(zalecane: {recommended})")
    
    return suggested


def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / 'config' / 'row_counts.json'
    
    print("=== Analiza i sugestie dla row_counts.json ===\n")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        current_counts = json.load(f)
    
    is_valid, errors, warnings = validate_row_counts(current_counts)
    
    print("Aktualna konfiguracja:")
    print(f"  Błędy: {len(errors)}")
    print(f"  Ostrzeżenia: {len(warnings)}\n")
    
    if errors or warnings:
        print("Sugerowane poprawki:\n")
        suggested = suggest_row_counts(current_counts)
        
        suggested_path = base_dir / 'config' / 'row_counts_suggested.json'
        with open(suggested_path, 'w', encoding='utf-8') as f:
            json.dump(suggested, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Sugerowane wartości zapisane do: {suggested_path}")
        print("  Możesz skopiować wartości do row_counts.json")
        
        print("\n=== Walidacja sugerowanych wartości ===")
        is_valid_suggested, errors_suggested, warnings_suggested = validate_row_counts(suggested)
        
        if errors_suggested:
            print("❌ Nadal występują błędy:")
            for error in errors_suggested:
                print(f"  - {error}")
        elif warnings_suggested:
            print("⚠️  Ostrzeżenia (niekrytyczne):")
            for warning in warnings_suggested:
                print(f"  - {warning}")
        else:
            print("✓ Sugerowane wartości są poprawne!")
    else:
        print("✓ Konfiguracja jest już poprawna, nie wymaga zmian.")


if __name__ == '__main__':
    main()

