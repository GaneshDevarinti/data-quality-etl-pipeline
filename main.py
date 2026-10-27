
import pandas as pd
import sqlite3
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "raw_sales.csv"
DB_FILE = BASE_DIR / "sales.db"

logging.basicConfig(
    filename=BASE_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

def extract():
    logging.info("Extracting raw sales data")
    return pd.read_csv(CSV_FILE)

def transform(df):
    df = df.copy()

    # Convert invalid numeric values into missing values
    for col in ["order_id", "quantity", "price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Identify invalid records
    missing = df[["order_id", "product", "quantity", "price"]].isna().any(axis=1)
    duplicate = df["order_id"].duplicated(keep="first")
    invalid_quantity = df["quantity"] <= 0
    invalid_price = df["price"] < 0

    # Save rejected records with reasons
    rejected = df[
        missing | duplicate | invalid_quantity | invalid_price
    ].copy()

    rejected["rejection_reason"] = ""

    for index in rejected.index:
        reasons = []

        if missing.loc[index]:
            reasons.append("Missing or invalid required value")
        if duplicate.loc[index]:
            reasons.append("Duplicate order ID")
        if invalid_quantity.loc[index]:
            reasons.append("Quantity must be positive")
        if invalid_price.loc[index]:
            reasons.append("Price cannot be negative")

        rejected.loc[index, "rejection_reason"] = "; ".join(reasons)

    # Keep only valid records
    clean = df[
        ~(missing | duplicate | invalid_quantity | invalid_price)
    ].copy()

    clean["revenue"] = clean["quantity"] * clean["price"]

    return clean, rejected

def load(clean, rejected):
    with sqlite3.connect(DB_FILE) as conn:
        clean.to_sql("sales", conn, if_exists="replace", index=False)
        rejected.to_sql("rejected_records", conn, if_exists="replace", index=False)

    logging.info(
        "Load completed: %s valid, %s rejected",
        len(clean), len(rejected)
    )

def main():
    raw = extract()
    clean, rejected = transform(raw)
    load(clean, rejected)

    print("Raw records:", len(raw))
    print("Clean records:", len(clean))
    print("Rejected records:", len(rejected))
    print("Total clean revenue:", clean["revenue"].sum())
    print("Database:", DB_FILE)
    print("Log file:", BASE_DIR / "pipeline.log")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Pipeline failed")
        raise
