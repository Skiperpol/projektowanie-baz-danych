from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, MetaData
import psycopg2
from typing import Dict

load_dotenv()

class DB:
    def __init__(self):
        self.host = os.getenv("PGHOST", "localhost")
        self.port = int(os.getenv("PGPORT", 5432))
        self.user = os.getenv("PGUSER", "postgres")
        self.password = os.getenv("PGPASSWORD", "")
        self.dbname = os.getenv("PGDATABASE", "postgres")
        self.batch_size = int(os.getenv("BATCH_SIZE", 50000))
        self.delete_all_data = os.getenv("DELETE_ALL_DATA", "false").lower() in ("true", "1", "yes")
        self.sqlalchemy_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        self.psycopg2_params = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "dbname": self.dbname,
        }
        self._engine = None
        self._meta = None

    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.sqlalchemy_url)
        return self._engine

    def metadata_reflect(self):
        if self._meta is None:
            m = MetaData()
            m.reflect(bind=self.engine())
            self._meta = m
        return self._meta

    def psycopg2_conn(self):
        return psycopg2.connect(**self.psycopg2_params)
    
    def delete_all_tables(self):
        """Truncate all tables - faster than DELETE and resets sequences"""
        conn = self.psycopg2_conn()
        cur = conn.cursor()
        
        meta = self.metadata_reflect()
        table_names = [table.name for table in meta.tables.values() if table.schema == 'public']
        
        print("\n=== Truncating all tables ===")
        try:
            if table_names:
                tables_str = ', '.join([f'"{name}"' for name in table_names])
                cur.execute(f'TRUNCATE TABLE {tables_str} CASCADE')
                print(f"  Truncated {len(table_names)} tables: {', '.join(table_names)}")
            else:
                print("  No tables found to truncate")
        except Exception as e:
            print(f"  Error: Could not truncate tables: {e}")
            for table_name in table_names:
                try:
                    cur.execute(f'TRUNCATE TABLE "{table_name}" CASCADE')
                    print(f"  Truncated {table_name}")
                except Exception as e2:
                    print(f"  Warning: Could not truncate {table_name}: {e2}")
        
        conn.commit()
        cur.close()
        conn.close()
        print("=== All tables truncated ===\n")
