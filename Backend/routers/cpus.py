from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import CPU
from schemas import CPUSchema

router = APIRouter(prefix="/cpus", tags=["CPUs"])


@router.get("/", response_model=list[CPUSchema])
def list_cpus(
    socket: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    min_cores: Optional[int] = Query(None),
    category: Optional[str] = Query("Desktop"),
    db: Session = Depends(get_db),
):
    query = db.query(CPU)
    if category:
        query = query.filter(CPU.category == category)
    if socket:
        query = query.filter(CPU.socket.ilike(f"%{socket}%"))
    if max_price is not None:
        query = query.filter(CPU.price <= max_price)
    if min_cores is not None:
        query = query.filter(CPU.cores >= min_cores)
    return query.all()