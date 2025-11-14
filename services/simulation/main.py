from fastapi import FastAPI
from sqlalchemy.orm import Session
from shared.database import get_db, Base, engine
from .routers import router
import sys

app = FastAPI(title="AFIN Simulation Service", docs_url="/docs")

# Создаём таблицы
try:
    from . import models  # Импортируем модели для создания таблиц
    Base.metadata.create_all(bind=engine)
    print("✅ Simulation service: Database tables created successfully")
except Exception as e:
    sys.stderr.write(f"❌ Simulation service: DB init failed: {e}\n")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "simulation"}