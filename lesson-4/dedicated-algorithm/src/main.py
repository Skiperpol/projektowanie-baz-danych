import json
import os
import sys
from pathlib import Path
from db import DB
from loaders import StreamLoader
from validators import validate_row_counts

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / 'config' / 'row_counts.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        row_counts = json.load(f)

    skip_validation = os.getenv("SKIP_VALIDATION", "false").lower() in ("true", "1", "yes")
    if not skip_validation:
        print("\n=== Walidacja konfiguracji row_counts.json ===")
        is_valid, errors, warnings = validate_row_counts(row_counts)
        
        if warnings:
            print("\n⚠️  Ostrzeżenia:")
            for warning in warnings:
                print(f"  - {warning}")
        
        if errors:
            print("\n❌ Błędy walidacji:")
            for error in errors:
                print(f"  - {error}")
            print("\n❌  Seedowanie nie zostanie rozpoczęte z powodu błędów walidacji.")
            print("   Aby pominąć walidację, ustaw zmienną środowiskową SKIP_VALIDATION=true")
            sys.exit(1)
        
        if not warnings and not errors:
            print("✓ Konfiguracja jest poprawna")
        print()

    db = DB()
    
    if db.delete_all_data:
        print("DELETE_ALL_DATA flag is set to true. Deleting all existing data...")
        db.delete_all_tables()
    
    loader = StreamLoader(db, row_counts)
    loader.load_all()
    print("All done.")

if __name__ == '__main__':
    main()
