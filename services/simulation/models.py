from sqlalchemy import Column, Integer, JSON, Float, String
from shared.database import Base

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, nullable=False)
    results = Column(JSON, nullable=False)
    duration = Column(Float, nullable=False)
    status = Column(String, default="running")