from sqlalchemy import Column, Integer, String, Boolean, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class GPU(Base):
    __tablename__ = "gpus"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer = Column(String(100))
    product_name = Column(String(255), nullable=False, unique=True)
    release_year = Column(Integer)
    mem_size_mb = Column(Integer)
    mem_bus_width = Column(Integer)
    gpu_clock_mhz = Column(Integer)
    mem_clock_mhz = Column(Integer)
    unified_shaders = Column(Integer)
    tmu = Column(Integer)
    rop = Column(Integer)
    pixel_shader = Column(Numeric(5, 2))
    vertex_shader = Column(Numeric(5, 2))
    igp = Column(Boolean)
    bus = Column(String(50))
    mem_type = Column(String(50))
    gpu_chip = Column(String(100))

    # Nullable — filled later by scraper
    gaming_1080p_score = Column(Integer, nullable=True)
    gaming_1440p_score = Column(Integer, nullable=True)
    gaming_4k_score = Column(Integer, nullable=True)
    compute_score = Column(Integer, nullable=True)
    current_price_usd = Column(Numeric(10, 2), nullable=True)

    last_updated = Column(TIMESTAMP, server_default=func.now())


class CPU(Base):
    __tablename__ = "cpus"

    id = Column(Integer, primary_key=True, index=True)
    cpu_name = Column(String(255), nullable=False, unique=True)
    price = Column(Numeric(10, 2))
    cpu_mark = Column(Integer)
    cpu_value = Column(Numeric(10, 4))
    thread_mark = Column(Integer)
    thread_value = Column(Numeric(10, 4))
    tdp_watts = Column(Integer)
    power_perf = Column(Numeric(10, 4))
    cores = Column(Integer)
    test_date = Column(String(20))
    socket = Column(String(50))
    category = Column(String(100))

    last_updated = Column(TIMESTAMP, server_default=func.now())