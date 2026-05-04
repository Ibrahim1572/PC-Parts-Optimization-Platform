"""
data_loader.py
Run once to populate the DB from CSV datasets.

Usage:
    python data_loader.py
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))

from database import engine, SessionLocal
from models import GPU, CPU, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

GPU_CSV = os.path.join(os.path.dirname(__file__), "data", "gpu_data.csv")
CPU_CSV = os.path.join(os.path.dirname(__file__), "data", "cpu_data.csv")


# ---------------------------------------------------------------------------
# Cleaners
# ---------------------------------------------------------------------------
def clean_int(val):
    try:
        v = float(str(val).strip())
        return int(v) if not pd.isna(v) else None
    except (ValueError, TypeError):
        return None


def clean_float(val):
    try:
        v = float(str(val).strip())
        return v if not pd.isna(v) else None
    except (ValueError, TypeError):
        return None


def clean_str(val):
    if pd.isna(val):
        return None
    return str(val).strip() or None


def clean_bool(val):
    if pd.isna(val):
        return False
    return str(val).strip().lower() in ("yes", "1", "true")


# ---------------------------------------------------------------------------
# Load GPUs
# ---------------------------------------------------------------------------
def load_gpus(db):
    df = pd.read_csv(GPU_CSV)
    df = df.drop_duplicates(subset=["productName"], keep="first")
    print(f"  GPU CSV rows: {len(df)}")

    loaded = 0
    skipped = 0

    for _, row in df.iterrows():
        product_name = clean_str(row.get("productName"))
        if not product_name:
            skipped += 1
            continue

        exists = db.query(GPU).filter(GPU.product_name == product_name).first()
        if exists:
            skipped += 1
            continue

        gpu = GPU(
            manufacturer=clean_str(row.get("manufacturer")),
            product_name=product_name,
            release_year=clean_int(row.get("releaseYear")),
            mem_size_mb=clean_int(row.get("memSize")),
            mem_bus_width=clean_int(row.get("memBusWidth")),
            gpu_clock_mhz=clean_int(row.get("gpuClock")),
            mem_clock_mhz=clean_int(row.get("memClock")),
            unified_shaders=clean_int(row.get("unifiedShader")),
            tmu=clean_int(row.get("tmu")),
            rop=clean_int(row.get("rop")),
            pixel_shader=clean_float(row.get("pixelShader")),
            vertex_shader=clean_float(row.get("vertexShader")),
            igp=clean_bool(row.get("igp")),
            bus=clean_str(row.get("bus")),
            mem_type=clean_str(row.get("memType")),
            gpu_chip=clean_str(row.get("gpuChip")),
        )
        db.add(gpu)
        loaded += 1

    db.commit()
    return loaded, skipped


# ---------------------------------------------------------------------------
# Load CPUs
# ---------------------------------------------------------------------------
def load_cpus(db):
    df = pd.read_csv(CPU_CSV)
    df = df.drop_duplicates(subset=["cpuName"], keep="first")
    print(f"  CPU CSV rows: {len(df)}")

    loaded = 0
    skipped = 0

    for _, row in df.iterrows():
        cpu_name = clean_str(row.get("cpuName"))
        if not cpu_name:
            skipped += 1
            continue

        exists = db.query(CPU).filter(CPU.cpu_name == cpu_name).first()
        if exists:
            skipped += 1
            continue

        cpu = CPU(
            cpu_name=cpu_name,
            price=clean_float(row.get("price")),
            cpu_mark=clean_int(row.get("cpuMark")),
            cpu_value=clean_float(row.get("cpuValue")),
            thread_mark=clean_int(row.get("threadMark")),
            thread_value=clean_float(row.get("threadValue")),
            tdp_watts=clean_int(row.get("TDP")),
            power_perf=clean_float(row.get("powerPerf")),
            cores=clean_int(row.get("cores")),
            test_date=clean_str(row.get("testDate")),
            socket=clean_str(row.get("socket")),
            category=clean_str(row.get("category")),
        )
        db.add(cpu)
        loaded += 1

    db.commit()
    return loaded, skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    db = SessionLocal()
    try:
        print("\n=== PC Build Optimizer — Data Loader ===\n")

        if not os.path.exists(GPU_CSV):
            print(f"[ERROR] GPU CSV not found at {GPU_CSV}")
            sys.exit(1)
        if not os.path.exists(CPU_CSV):
            print(f"[ERROR] CPU CSV not found at {CPU_CSV}")
            sys.exit(1)

        print("Loading GPUs...")
        gpu_loaded, gpu_skipped = load_gpus(db)
        print(f"  ✓ Loaded {gpu_loaded} GPUs (skipped {gpu_skipped})\n")

        print("Loading CPUs...")
        cpu_loaded, cpu_skipped = load_cpus(db)
        print(f"  ✓ Loaded {cpu_loaded} CPUs (skipped {cpu_skipped})\n")

        print(f"=== Done: {gpu_loaded} GPUs + {cpu_loaded} CPUs inserted ===\n")

    finally:
        db.close()