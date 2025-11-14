from sqlalchemy.orm import Session
from .models import ProcessModel
from .schemas import ModelCreate, ModelUpdate

def create_model(db: Session, model_in: ModelCreate):
    db_model = ProcessModel(**model_in.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def get_model(db: Session, model_id: int):
    return db.query(ProcessModel).filter(ProcessModel.id == model_id).first()

def get_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProcessModel).offset(skip).limit(limit).all()

def update_model(db: Session, model_id: int, model_in: ModelUpdate):
    db_model = get_model(db, model_id)
    if not db_model:
        return None
    update_data = model_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_model, key, value)
    db.commit()
    db.refresh(db_model)
    return db_model

def delete_model(db: Session, model_id: int):
    db_model = get_model(db, model_id)
    if db_model:
        db.delete(db_model)
        db.commit()
    return db_model