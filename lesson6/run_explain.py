import psycopg2
from datetime import datetime
from lesson5.queries import QUERIES
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "explain_logs.txt")

def log(text):
    """Append text to log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")


def run_explain_queries():
    conn = psycopg2.connect(
        host="projectdatabase.cjy06esawu7e.eu-west-3.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="ciyoJLyVTY1dyCTGkAws"
    )
    cur = conn.cursor()

    # Nagłówek logu
    log("=" * 120)
    log(f"START EXPLAIN RUN — {datetime.now()}")
    log("=" * 120)

    
    for idx, (title, query) in QUERIES.items():
        if "%s" in query:
            query = query.replace("%s", "'%test%'")
        header = f"\n\n{'=' * 50}\nEXPLAIN ANALYZE — Query {idx}: {title}\n{'=' * 50}"
        print(header)
        log(header)

        explain_query = "EXPLAIN ANALYZE " + query

        try:
            cur.execute(explain_query)
            result = cur.fetchall()

            for row in result:
                print(row[0])
                log(row[0])

        except Exception as e:
            err_msg = f"[ERROR EXECUTING QUERY {idx}] {e}"
            print(err_msg)
            log(err_msg)

    cur.close()
    conn.close()

    log(f"\nFINISHED — {datetime.now()}")
    log("=" * 120)


if __name__ == "__main__":
    run_explain_queries()
