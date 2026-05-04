"""
score_loader.py
Run once to update GPU benchmark scores from gpu_performance_data.csv

Usage:
    python score_loader.py
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal
from models import GPU

SCORE_CSV = os.path.join(os.path.dirname(__file__), "data", "gpu_performance_data.csv")


def clean_int(val):
    try:
        v = float(str(val).strip())
        return int(v) if not pd.isna(v) else None
    except (ValueError, TypeError):
        return None


def load_scores(db):
    df = pd.read_csv(SCORE_CSV)
    print(f"  Score CSV rows: {len(df)}")

    updated = 0
    not_found = 0

    for _, row in df.iterrows():
        gpu_name = str(row.get("gpu_name", "")).strip()
        if not gpu_name:
            continue

        gpu = db.query(GPU).filter(GPU.product_name == gpu_name).first()
        if not gpu:
            print(f"  [NOT FOUND] {gpu_name}")
            not_found += 1
            continue

        gpu.gaming_1080p_score = clean_int(row.get("1080p_gaming_score"))
        gpu.gaming_1440p_score = clean_int(row.get("1440p_gaming_score"))
        gpu.gaming_4k_score    = clean_int(row.get("4k_gaming_score"))
        gpu.compute_score      = clean_int(row.get("ml_workload_score"))
        updated += 1

    db.commit()
    return updated, not_found


if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("\n=== PC Build Optimizer — Score Loader ===\n")

        if not os.path.exists(SCORE_CSV):
            print(f"[ERROR] CSV not found at {SCORE_CSV}")
            sys.exit(1)

        print("Updating GPU scores...")
        updated, not_found = load_scores(db)
        print(f"  ✓ Updated {updated} GPUs")
        print(f"  ✗ Not found in DB: {not_found}")
        print("\n=== Done ===\n")

    finally:
        db.close()