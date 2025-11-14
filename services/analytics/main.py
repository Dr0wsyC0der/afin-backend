from fastapi import FastAPI
from .routers import router
import sys

app = FastAPI(title="ANALYTICS Service", docs_url="/docs")

try:
    app.include_router(router)
except Exception as e:
    sys.stderr.write(f"Warning: No routers: {e}\n")

@app.get("/health")
def health():
    return {"status": "ok", "service": "analytics"}
