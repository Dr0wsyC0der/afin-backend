from fastapi import FastAPI
from shared.database import Base, engine
from routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Service", docs_url="/docs")
app.include_router(router)