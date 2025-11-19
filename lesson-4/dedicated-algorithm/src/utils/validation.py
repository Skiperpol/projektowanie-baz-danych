import os
import sys

def should_skip_validation() -> bool:
    """Checks the environment variable SKIP_VALIDATION."""
    return os.getenv("SKIP_VALIDATION", "false").lower() in ("true", "1", "yes")


def run_validation(row_counts, filename: str = "row_counts.json") -> None:
    """
    Runs the validation process.
    Exits program if validation fails.
    """
    from utils.validators import validate_row_counts

    print(f"\n=== Walidacja konfiguracji {filename} ===")
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
        print("Konfiguracja jest poprawna!")
    print()
