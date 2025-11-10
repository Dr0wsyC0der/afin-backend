from fastapi import FastAPI

app = FastAPI(title="ANALYTICS Service", docs_url="/docs")

try:
    from routers import router
    app.include_router(router)
except Exception as e:
    import sys
    sys.stderr.write(f"Warning: No routers in $s: {e}\n")

@app.get("/health")
def health():
    return {"status": "ok", "service": "analytics"}
