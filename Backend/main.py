from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Literal

from database import get_db, engine
from models import GPU, CPU
import models
from schemas import RecommendResponse, HealthResponse, StatsResponse, ComboResult
from routers import gpus, cpus
from services.recommender import get_recommendations

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PC Build Optimizer API",
    description="Budget-aware GPU + CPU combo recommendations.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(gpus.router)
app.include_router(cpus.router)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["Meta"])
def health():
    return {"status": "ok"}


@app.get("/datasets/stats", response_model=StatsResponse, tags=["Meta"])
def dataset_stats(db: Session = Depends(get_db)):
    return {
        "total_gpus": db.query(GPU).count(),
        "total_cpus": db.query(CPU).count(),
    }


@app.get("/recommend", response_model=RecommendResponse, tags=["Recommendations"])
def recommend(
    budget_usd: float = Query(..., gt=0, description="Total budget in USD"),
    use_case: Literal[
        "gaming_1080p", "gaming_1440p", "gaming_4k", "ml_compute", "general"
    ] = Query(...),
    gpu_budget_split: float = Query(0.6, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
):
    results = get_recommendations(
        db=db,
        budget_usd=budget_usd,
        use_case=use_case,
        gpu_budget_split=gpu_budget_split,
    )

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No valid combos found for this budget. Try a higher budget.",
        )

    combo_results = [
        ComboResult(
            gpu=r["gpu"],
            cpu=r["cpu"],
            total_price=r["total_price"],
            combo_score=r["combo_score"],
            reason=r["reason"],
            gpu_budget=r["gpu_budget"],
            cpu_budget=r["cpu_budget"],
        )
        for r in results
    ]

    return RecommendResponse(
        use_case=use_case,
        budget_usd=budget_usd,
        gpu_budget_split=gpu_budget_split,
        results=combo_results,
    )