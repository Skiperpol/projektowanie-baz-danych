import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from queries import QUERIES

# 1️⃣ Wczytanie zmiennych środowiskowych
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)

# 2️⃣ Funkcja wykonująca zapytanie
def execute_query(query, params=None):
    try:
        with psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        ) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                results = cur.fetchall()
                return results
    except Exception as e:
        print("Błąd połączenia lub zapytania:", e)
        return []

# 3️⃣ Funkcja drukująca wyniki
def print_results(results):
    if not results:
        print("Brak wyników.")
        return
    for row in results:
        print(row)
    print(f"\nLiczba rekordów: {len(results)}\n")

# 4️⃣ Menu użytkownika
def main():
    print("=== Raporty SQL ===")
    for key, (desc, _) in QUERIES.items():
        print(f"{key}. {desc}")
    print("0. Wszystkie zapytania")

    choice = input("Wybierz numer zapytania (0 = wszystkie): ").strip()
    if choice == "0":
        for key, (_, query) in QUERIES.items():
            print(f"\n--- Zapytanie {key}: {QUERIES[key][0]} ---")
            results = execute_query(query)
            print_results(results)
    else:
        try:
            num = int(choice)
            if num in QUERIES:
                print(f"\n--- Zapytanie {num}: {QUERIES[num][0]} ---")
                if "%s" in QUERIES[num][1]:
                    param = input("Podaj wartość do wyszukiwania: ")
                    results = execute_query(QUERIES[num][1], (param, param))
                else:
                    results = execute_query(QUERIES[num][1])
                print_results(results)
            else:
                print("Niepoprawny numer zapytania.")
        except ValueError:
            print("Niepoprawny wybór.")

if __name__ == "__main__":
    main()
