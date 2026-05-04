"""
services/recommender.py
v1: rule-based heuristic engine — ML model planned for v2
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import GPU, CPU


# ---------------------------------------------------------------------------
# Use case configuration
# ---------------------------------------------------------------------------
USE_CASE_CONFIG = {
    "gaming_1080p": {
        "gpu_weight": 0.65,
        "cpu_weight": 0.35,
        "gpu_score_field": "gaming_1080p_score",
        "cpu_score_field": "thread_mark",
        "reason_template": (
            "{gpu_name} ({shaders} shaders, {mem}MB VRAM) paired with "
            "{cpu_name} ({thread_mark} thread mark) — optimized for 1080p gaming."
        ),
    },
    "gaming_1440p": {
        "gpu_weight": 0.70,
        "cpu_weight": 0.30,
        "gpu_score_field": "gaming_1440p_score",
        "cpu_score_field": "thread_mark",
        "reason_template": (
            "{gpu_name} ({shaders} shaders, {mem}MB VRAM) leads this 1440p build — "
            "{cpu_name} keeps up without bottlenecking."
        ),
    },
    "gaming_4k": {
        "gpu_weight": 0.75,
        "cpu_weight": 0.25,
        "gpu_score_field": "gaming_4k_score",
        "cpu_score_field": "thread_mark",
        "reason_template": (
            "4K is GPU-bound — {gpu_name} ({mem}MB VRAM) prioritized. "
            "{cpu_name} handles game logic without overspending."
        ),
    },
    "ml_compute": {
        "gpu_weight": 0.55,
        "cpu_weight": 0.45,
        "gpu_score_field": "compute_score",
        "cpu_score_field": "cpu_mark",
        "reason_template": (
            "{gpu_name} ({mem}MB VRAM) for GPU workloads — "
            "{cpu_name} ({cpu_mark} PassMark) handles CPU-side preprocessing."
        ),
    },
    "general": {
        "gpu_weight": 0.60,
        "cpu_weight": 0.40,
        "gpu_score_field": "gaming_1080p_score",
        "cpu_score_field": "cpu_mark",
        "reason_template": (
            "Balanced build — {gpu_name} for graphics, "
            "{cpu_name} ({cpu_mark} PassMark) for everyday multitasking."
        ),
    },
}

# ---------------------------------------------------------------------------
# Consumer GPU name prefixes
# ---------------------------------------------------------------------------
GPU_PREFIXES = (
    "GeForce RTX",
    "GeForce GTX",
    "TITAN",
    "Radeon RX",
    "Radeon VII",
    "Intel Arc",
)

# ---------------------------------------------------------------------------
# Valid CPU sockets
# ---------------------------------------------------------------------------
CPU_SOCKETS = (
    "AM4",
    "FCLGA1151-2",
    "FCLGA1700",
    "LGA 1700",
    "FCLGA1200",
)

# ---------------------------------------------------------------------------
# Valid CPU test dates
# ---------------------------------------------------------------------------
CPU_DATES = ("2018", "2019", "2020", "2021", "2022")


# ---------------------------------------------------------------------------
# Normalizer — min-max scale to [0, 1]
# ---------------------------------------------------------------------------
def _normalize(values: list) -> list:
    clean = [v if v is not None else 0.0 for v in values]
    lo, hi = min(clean), max(clean)
    if hi == lo:
        return [0.5] * len(clean)
    return [(v - lo) / (hi - lo) for v in clean]


# ---------------------------------------------------------------------------
# Reason string builder
# ---------------------------------------------------------------------------
def _build_reason(gpu: GPU, cpu: CPU, config: dict) -> str:
    return config["reason_template"].format(
        gpu_name=gpu.product_name,
        shaders=gpu.unified_shaders or "N/A",
        mem=gpu.mem_size_mb or "N/A",
        cpu_name=cpu.cpu_name,
        thread_mark=cpu.thread_mark or "N/A",
        cpu_mark=cpu.cpu_mark or "N/A",
    )


# ---------------------------------------------------------------------------
# Main recommendation function
# ---------------------------------------------------------------------------
def get_recommendations(
    db: Session,
    budget_usd: float,
    use_case: str,
    gpu_budget_split: float = 0.6,
    top_n: int = 3,
) -> list:

    if use_case not in USE_CASE_CONFIG:
        raise ValueError(f"Invalid use_case. Choose from: {list(USE_CASE_CONFIG)}")

    config = USE_CASE_CONFIG[use_case]
    gpu_budget = round(budget_usd * gpu_budget_split, 2)
    cpu_budget = round(budget_usd * (1 - gpu_budget_split), 2)

    # ------------------------------------------------------------------
    # 1. Fetch filtered GPUs and CPUs
    # ------------------------------------------------------------------
    all_gpus = db.query(GPU).filter(
        GPU.igp == False,
        GPU.product_name.notlike("%Mobile%"),
        GPU.release_year > 2018,
        or_(*[GPU.product_name.ilike(f"{p}%") for p in GPU_PREFIXES])
    ).all()

    all_cpus = db.query(CPU).filter(
        CPU.category == "Desktop",
        CPU.socket.in_(CPU_SOCKETS),
        CPU.test_date.in_(CPU_DATES),
    ).all()

    # ------------------------------------------------------------------
    # 2. Filter by budget
    #    GPUs: no price data yet — include all
    #    CPUs: filter by price
    # ------------------------------------------------------------------
    gpus_in_budget = [
        g for g in all_gpus
        if g.current_price_usd is None or float(g.current_price_usd) <= gpu_budget
    ]
    cpus_in_budget = [
        c for c in all_cpus
        if c.price is not None and float(c.price) <= cpu_budget
    ]

    if not gpus_in_budget or not cpus_in_budget:
        return []

    # ------------------------------------------------------------------
    # 3. Get raw scores — no nulls expected from these filtered sets
    # ------------------------------------------------------------------
    gpu_score_field = config["gpu_score_field"]
    cpu_score_field = config["cpu_score_field"]

    gpu_raw = {
        g.id: float(getattr(g, gpu_score_field))
        for g in gpus_in_budget
    }
    cpu_raw = {
        c.id: float(getattr(c, cpu_score_field))
        for c in cpus_in_budget
    }

    # ------------------------------------------------------------------
    # 4. Normalize both score sets to [0, 1]
    # ------------------------------------------------------------------
    gpu_vals = list(gpu_raw.values())
    gpu_lo, gpu_hi = min(gpu_vals), max(gpu_vals)
    gpu_norm = {
        gid: (v - gpu_lo) / (gpu_hi - gpu_lo) if gpu_hi != gpu_lo else 0.5
        for gid, v in gpu_raw.items()
    }

    cpu_vals = list(cpu_raw.values())
    cpu_lo, cpu_hi = min(cpu_vals), max(cpu_vals)
    cpu_norm = {
        cid: (v - cpu_lo) / (cpu_hi - cpu_lo) if cpu_hi != cpu_lo else 0.5
        for cid, v in cpu_raw.items()
    }

    # ------------------------------------------------------------------
    # 5. Score every GPU+CPU pair
    # ------------------------------------------------------------------
    gpu_w = config["gpu_weight"]
    cpu_w = config["cpu_weight"]

    combos = []
    for gpu in gpus_in_budget:
        for cpu in cpus_in_budget:
            combo_score = (
                gpu_w * gpu_norm[gpu.id]
                + cpu_w * cpu_norm[cpu.id]
            )

            # Small value bonus for staying under budget (max +0.05)
            cpu_price = float(cpu.price) if cpu.price else 0.0
            total_price = gpu_budget + cpu_price
            headroom = (budget_usd - total_price) / budget_usd
            combo_score += min(0.05, max(0.0, headroom * 0.1))

            combos.append({
                "gpu": gpu,
                "cpu": cpu,
                "combo_score": round(combo_score, 4),
                "total_price": round(total_price, 2),
                "gpu_budget": gpu_budget,
                "cpu_budget": cpu_budget,
                "reason": _build_reason(gpu, cpu, config),
            })

    # ------------------------------------------------------------------
    # 6. Sort and return top N
    # ------------------------------------------------------------------
    combos.sort(key=lambda x: x["combo_score"], reverse=True)
    return combos[:top_n]