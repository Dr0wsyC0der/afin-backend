from pydantic import BaseModel
from typing import Dict, Any

class SimulationRequest(BaseModel):
    model_id: int
    model_data: Dict[str, Any]

class SimulationOut(BaseModel):
    id: int
    model_id: int
    results: Dict[str, Any] | None = None
    duration: float | None = None
    status: str = "running"

    class Config:
        from_attributes = True