from sqlalchemy import Column, Integer, String, JSON
from shared.database import Base

class ProcessModel(Base):
    __tablename__ = "process_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)  # BPMN в JSON
    user_id = Column(Integer, nullable=False)