import json
import os
import sys
from pathlib import Path
from utils.db import DB
from utils.loader import StreamLoader
from utils.validators import validate_row_counts
from utils.validation import run_validation, should_skip_validation

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / 'config' / 'row_counts.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        row_counts = json.load(f)

    if not should_skip_validation():
        run_validation(row_counts)

    db = DB()
    
    if db.delete_all_data:
        print("DELETE_ALL_DATA flag is set to true. Deleting all existing data...")
        db.delete_all_tables()
    
    loader = StreamLoader(db, row_counts)
    loader.load_all()
    print("All done!")

if __name__ == '__main__':
    main()
