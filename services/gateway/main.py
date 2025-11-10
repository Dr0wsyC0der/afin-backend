from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="AFIN API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "auth": "http://auth:8000",
    "models": "http://models:8000",
    "simulation": "http://simulation:8000",
}

@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, service: str, path: str):
    if service not in SERVICES:
        return {"error": "Service not found"}
    url = f"{SERVICES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            content=await request.body(),
            params=request.query_params,
        )
        return resp.json() if "application/json" in resp.headers.get("content-type", "") else resp.text