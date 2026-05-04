from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import GPU
from schemas import GPUSchema

router = APIRouter(prefix="/gpus", tags=["GPUs"])


@router.get("/", response_model=list[GPUSchema])
def list_gpus(
    manufacturer: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    min_mem_size: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(GPU)
    if manufacturer:
        query = query.filter(GPU.manufacturer.ilike(f"%{manufacturer}%"))
    if max_price is not None:
        query = query.filter(GPU.current_price_usd <= max_price)
    if min_mem_size is not None:
        query = query.filter(GPU.mem_size_mb >= min_mem_size)
    return query.all()