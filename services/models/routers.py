from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from shared.database import get_db
from . import crud, schemas
from .utils.bpmn import bpmn_to_json, json_to_bpmn

router = APIRouter()
@router.get("/health")
def health():
    return {"status": "ok", "service": "models"}

@router.post("/", response_model=schemas.ModelOut)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    return crud.create_model(db, model)

@router.get("/", response_model=list[schemas.ModelOut])
def list_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_models(db, skip, limit)

@router.get("/{model_id}", response_model=schemas.ModelOut)
def get_model(model_id: int, db: Session = Depends(get_db)):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")
    return model

@router.put("/{model_id}", response_model=schemas.ModelOut)
def update_model(model_id: int, model_in: schemas.ModelUpdate, db: Session = Depends(get_db)):
    updated = crud.update_model(db, model_id, model_in)
    if not updated:
        raise HTTPException(404, "Model not found")
    return updated

@router.delete("/{model_id}")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_model(db, model_id)
    if not deleted:
        raise HTTPException(404, "Model not found")
    return {"detail": "Deleted"}

# === BPMN импорт ===
@router.post("/import/bpmn")
async def import_bpmn(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    try:
        json_data = bpmn_to_json(content.decode())
        model_in = schemas.ModelCreate(
            name=file.filename,
            data=json_data,
            user_id=1  # Заглушка
        )
        return crud.create_model(db, model_in)
    except Exception as e:
        raise HTTPException(400, f"BPMN parse error: {str(e)}")

# === BPMN экспорт ===
@router.get("/{model_id}/export/bpmn")
def export_bpmn(model_id: int, db: Session = Depends(get_db)):
    model = crud.get_model(db, model_id)
    if not model:
        raise HTTPException(404, "Model not found")
    xml = json_to_bpmn(model.data)
    return Response(
        content=xml,
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename=model_{model_id}.bpmn"}
    )