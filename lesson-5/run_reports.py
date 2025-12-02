import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from queries import QUERIES

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

def execute_query(query, params=None):
    try:
        with psycopg2.connect(
            host="projectdatabase.cjy06esawu7e.eu-west-3.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="ciyoJLyVTY1dyCTGkAws",
            port=5432
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                headers = [desc[0] for desc in cur.description] if cur.description else []
                results = cur.fetchall()
                return results, headers
    except Exception as e:
        print("Błąd połączenia lub zapytania:", e)
        return [], []

def print_results(results, headers=None):
    if not results:
        print("Brak wyników.")
        return

    if tabulate:
        if isinstance(results[0], dict):
            ordered_headers = headers or list(results[0].keys())
            rows = [[row.get(h) for h in ordered_headers] for row in results]
            print(tabulate(rows, headers=ordered_headers, tablefmt="grid"))
        else:
            print(tabulate(results, headers=headers if headers else (), tablefmt="grid"))
    else:
        for row in results:
            print(row)
    print(f"\nLiczba rekordów: {len(results)}\n")

def main():
    print("=== Raporty SQL ===")
    for key, (desc, _) in QUERIES.items():
        print(f"{key}. {desc}")
    print("0. Wszystkie zapytania")

    choice = input("Wybierz numer zapytania (0 = wszystkie): ").strip()
    if choice == "0":
        for key, (_, query) in QUERIES.items():
            print(f"\n--- Zapytanie {key}: {QUERIES[key][0]} ---")
            results, headers = execute_query(query)
            print_results(results, headers)
    else:
        try:
            num = int(choice)
            if num in QUERIES:
                print(f"\n--- Zapytanie {num}: {QUERIES[num][0]} ---")
                if "%s" in QUERIES[num][1]:
                    param = input("Podaj wartość do wyszukiwania: ")
                    search_pattern = f"%{param}%"
                    results, headers = execute_query(QUERIES[num][1], (search_pattern, search_pattern))
                else:
                    results, headers = execute_query(QUERIES[num][1])
                print_results(results, headers)
            else:
                print("Niepoprawny numer zapytania.")
        except ValueError:
            print("Niepoprawny wybór.")

if __name__ == "__main__":
    main()
