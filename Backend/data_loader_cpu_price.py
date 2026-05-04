"""
price_loader_cpu.py
Run once to update CPU prices from cpu_price.csv

Usage:
    python price_loader_cpu.py
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import CPU

PRICE_CSV = os.path.join(os.path.dirname(__file__), "data", "cpu_price.csv")


def clean_float(val):
    try:
        v = float(str(val).strip().replace(",", ""))
        return v if not pd.isna(v) else None
    except (ValueError, TypeError):
        return None


def load_cpu_prices(db):
    df = pd.read_csv(PRICE_CSV)
    print(f"  Price CSV rows: {len(df)}")

    updated = 0
    not_found = 0

    for _, row in df.iterrows():
        cpu_name = str(row.get("cpu_name", "")).strip()
        if not cpu_name:
            continue

        cpu = db.query(CPU).filter(CPU.cpu_name == cpu_name).first()
        if not cpu:
            print(f"  [NOT FOUND] {cpu_name}")
            not_found += 1
            continue

        cpu.price = clean_float(row.get("price_usd"))
        updated += 1

    db.commit()
    return updated, not_found


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("\n=== PC Build Optimizer — CPU Price Loader ===\n")

        if not os.path.exists(PRICE_CSV):
            print(f"[ERROR] CSV not found at {PRICE_CSV}")
            sys.exit(1)

        print("Updating CPU prices...")
        updated, not_found = load_cpu_prices(db)
        print(f"  ✓ Updated: {updated} CPUs")
        print(f"  ✗ Not found in DB: {not_found}")
        print("\n=== Done ===\n")

    finally:
        db.close()