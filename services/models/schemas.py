from pydantic import BaseModel
from typing import Dict, Any

class ModelBase(BaseModel):
    name: str
    data: Dict[str, Any]
    user_id: int

class ModelCreate(ModelBase):
    pass

class ModelUpdate(BaseModel):
    name: str | None = None
    data: Dict[str, Any] | None = None

class ModelOut(ModelBase):
    id: int

    class Config:
        from_attributes = True