# services/auth/main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from shared.database import get_db, Base, engine
from .routers import router
from . import models  # Импортируем модели для создания таблиц
import sys

app = FastAPI(title="AUTH Service", docs_url="/docs")

# Создаём таблицы
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Auth service: Database tables created successfully")
except Exception as e:
    sys.stderr.write(f"❌ Auth service: DB init failed: {e}\n")

try:
    app.include_router(router)
except Exception as e:
    sys.stderr.write(f"Warning: No routers: {e}\n")

@app.get("/health")
def health():
    return {"status": "ok", "service": "auth"}