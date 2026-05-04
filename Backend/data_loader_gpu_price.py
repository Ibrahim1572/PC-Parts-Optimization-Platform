"""
price_loader_gpu.py
Run once to update GPU prices from gpu_price.csv

Usage:
    python price_loader_gpu.py
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import GPU

PRICE_CSV = os.path.join(os.path.dirname(__file__), "data", "gpu_price.csv")


def clean_float(val):
    try:
        v = float(str(val).strip().replace(",", ""))
        return v if not pd.isna(v) else None
    except (ValueError, TypeError):
        return None


def load_gpu_prices(db):
    df = pd.read_csv(PRICE_CSV)
    print(f"  Price CSV rows: {len(df)}")

    updated = 0
    not_found = 0

    for _, row in df.iterrows():
        gpu_name = str(row.get("GPU Name", "")).strip()
        if not gpu_name:
            continue

        gpu = db.query(GPU).filter(GPU.product_name == gpu_name).first()
        if not gpu:
            print(f"  [NOT FOUND] {gpu_name}")
            not_found += 1
            continue

        gpu.current_price_usd = clean_float(row.get("Price (USD)"))
        updated += 1

    db.commit()
    return updated, not_found


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("\n=== PC Build Optimizer — GPU Price Loader ===\n")

        if not os.path.exists(PRICE_CSV):
            print(f"[ERROR] CSV not found at {PRICE_CSV}")
            sys.exit(1)

        print("Updating GPU prices...")
        updated, not_found = load_gpu_prices(db)
        print(f"  ✓ Updated: {updated} GPUs")
        print(f"  ✗ Not found in DB: {not_found}")
        print("\n=== Done ===\n")

    finally:
        db.close()