from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from shared.database import get_db
from .engine.simulator import run_simulation
from . import crud, schemas

router = APIRouter()

@router.get("/health")  # ВВЕРХУ!
def health():
    return {"status": "ok", "service": "simulation"}
@router.post("/", response_model=schemas.SimulationOut)
def start_simulation(
    request: schemas.SimulationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Запуск в фоне
    run = crud.create_run(db, request.model_id)
    background_tasks.add_task(crud.run_and_save, db, run.id, request.model_data)
    return run

@router.get("/{run_id}", response_model=schemas.SimulationOut)
def get_result(run_id: int, db: Session = Depends(get_db)):
    run = crud.get_run(db, run_id)
    if not run:
        raise HTTPException(404, "Simulation not found")
    return run