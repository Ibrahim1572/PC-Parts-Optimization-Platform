from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class GPUSchema(BaseModel):
    id: int
    manufacturer: Optional[str] = None
    product_name: str
    release_year: Optional[int] = None
    mem_size_mb: Optional[int] = None
    mem_bus_width: Optional[int] = None
    gpu_clock_mhz: Optional[int] = None
    mem_clock_mhz: Optional[int] = None
    unified_shaders: Optional[int] = None
    tmu: Optional[int] = None
    rop: Optional[int] = None
    pixel_shader: Optional[Decimal] = None
    vertex_shader: Optional[Decimal] = None
    igp: Optional[bool] = None
    bus: Optional[str] = None
    mem_type: Optional[str] = None
    gpu_chip: Optional[str] = None
    gaming_1080p_score: Optional[int] = None
    gaming_1440p_score: Optional[int] = None
    gaming_4k_score: Optional[int] = None
    compute_score: Optional[int] = None
    current_price_usd: Optional[Decimal] = None

    class Config:
        from_attributes = True


class CPUSchema(BaseModel):
    id: int
    cpu_name: str
    price: Optional[Decimal] = None
    cpu_mark: Optional[int] = None
    cpu_value: Optional[Decimal] = None
    thread_mark: Optional[int] = None
    thread_value: Optional[Decimal] = None
    tdp_watts: Optional[int] = None
    power_perf: Optional[Decimal] = None
    cores: Optional[int] = None
    test_date: Optional[str] = None
    socket: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True


class ComboResult(BaseModel):
    gpu: GPUSchema
    cpu: CPUSchema
    total_price: Optional[Decimal] = None
    combo_score: float
    reason: str
    gpu_budget: float
    cpu_budget: float


class RecommendResponse(BaseModel):
    use_case: str
    budget_usd: float
    gpu_budget_split: float
    results: list[ComboResult]


class HealthResponse(BaseModel):
    status: str


class StatsResponse(BaseModel):
    total_gpus: int
    total_cpus: int