import os
import logging
from pathlib import Path
import json
from datetime import datetime
from seeder import Seeder
from fk_resolver import find_table_dependencies, topological_sort
from dotenv import load_dotenv

load_dotenv()
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    filename=LOG_DIR / f"seed_report_{timestamp}.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

def load_schema(path="config/database_schema.json"):
    base_dir = Path(__file__).parent.parent
    schema_path = base_dir / path
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    return schema["tables"]

def main():
    logging.info("Seed Tool started")
    tables = load_schema()
    table_dependencies = find_table_dependencies(tables)
    order = topological_sort(tables, table_dependencies)
    logging.info("Seed order: %s", ", ".join(order))

    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_DATABASE", "testdb"),
    }

    seeder = Seeder(tables, order, db_config, logger=logging.getLogger())
    seeder.run()

if __name__ == "__main__":
    main()
