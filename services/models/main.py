from fastapi import FastAPI
from sqlalchemy.orm import Session
from shared.database import get_db, Base, engine
from .routers import router
import sys

app = FastAPI(title="MODELS Service", docs_url="/docs")

# Создаём таблицы
try:
    from . import models  # Импортируем модели для создания таблиц
    Base.metadata.create_all(bind=engine)
    print("✅ Models service: Database tables created successfully")
except Exception as e:
    sys.stderr.write(f"❌ Models service: DB init failed: {e}\n")

try:
    app.include_router(router)
except Exception as e:
    sys.stderr.write(f"Warning: No routers: {e}\n")

@app.get("/health")
def health():
    return {"status": "ok", "service": "models"}
