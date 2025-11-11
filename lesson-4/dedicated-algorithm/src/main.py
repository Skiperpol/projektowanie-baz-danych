import json
from pathlib import Path
from db import DB
from loaders import StreamLoader

def main():
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / 'config' / 'row_counts.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        row_counts = json.load(f)

    db = DB()
    
    if db.delete_all_data:
        print("DELETE_ALL_DATA flag is set to true. Deleting all existing data...")
        db.delete_all_tables()
    
    loader = StreamLoader(db, row_counts)
    loader.load_all()
    print("All done.")

if __name__ == '__main__':
    main()
