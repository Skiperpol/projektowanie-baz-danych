from dotenv import load_dotenv
import os
import psycopg2
from typing import Dict

load_dotenv()

class DB:
    def __init__(self):
        self.host = os.getenv("PGHOST", "localhost")
        self.port = int(os.getenv("PGPORT", 5432))
        self.user = os.getenv("PGUSER", "postgres")
        self.password = os.getenv("PGPASSWORD", "postgres")
        self.dbname = os.getenv("PGDATABASE", "postgres")
        self.batch_size = int(os.getenv("BATCH_SIZE", 50000))
        self.delete_all_data = os.getenv("DELETE_ALL_DATA", "false").lower() in ("true", "1", "yes")
        self.psycopg2_params = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "dbname": self.dbname,
        }

    def psycopg2_conn(self):
        return psycopg2.connect(**self.psycopg2_params)
    
    def delete_all_tables(self):
        """Truncate all tables - faster than DELETE and resets sequences"""
        conn = self.psycopg2_conn()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        table_rows = cur.fetchall()
        table_names = [row[0] for row in table_rows]
        
        print("\n=== Truncating all tables ===")
        if not table_names:
            print("  No tables found to truncate")
        else:
            try:
                tables_str = ', '.join([f'"{name}"' for name in table_names])
                cur.execute(f'TRUNCATE TABLE {tables_str} CASCADE')
                print(f"  Truncated {len(table_names)} tables")
            except Exception as e:
                print(f"  Error: Could not truncate tables together: {e}")
                print("  Trying to truncate tables individually...")
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
