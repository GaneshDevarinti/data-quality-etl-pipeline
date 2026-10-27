
import sqlite3
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent / "sales.db"

with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sales")
    print("Clean records in database:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM rejected_records")
    print("Rejected records in database:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT product, revenue
        FROM sales
        ORDER BY revenue DESC
    """)

    print("\nClean sales records:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("""
        SELECT rejection_reason, COUNT(*)
        FROM rejected_records
        GROUP BY rejection_reason
    """)

    print("\nRejection summary:")
    for row in cursor.fetchall():
        print(row)
