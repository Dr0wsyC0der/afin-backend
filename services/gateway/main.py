# services/gateway/main.py
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="AFIN API Gateway", docs_url="/docs")

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
    "analytics": "http://analytics:8000",
}

@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, service: str, path: str):
    if service not in SERVICES:
        raise HTTPException(404, "Service not found")
    url = f"{SERVICES[service]}/{path}"
    
    # Убираем заголовки, которые не должны передаваться
    headers = dict(request.headers)
    headers.pop("host", None)
    headers.pop("content-length", None)
    
    # Получаем тело запроса
    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0,
            )
            # Проверяем content-type для правильного возврата
            content_type = resp.headers.get("content-type", "")
            
            # Если ответ JSON (включая ошибки от FastAPI)
            if "json" in content_type:
                try:
                    json_data = resp.json()
                    # Возвращаем JSON с правильным статус кодом
                    return JSONResponse(
                        content=json_data,
                        status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() 
                                if k.lower() not in ['content-length', 'connection', 'server']}
                    )
                except Exception:
                    # Если не удалось распарсить JSON, возвращаем как текст
                    return Response(
                        content=resp.content,
                        status_code=resp.status_code,
                        media_type=content_type,
                        headers={k: v for k, v in resp.headers.items() 
                                if k.lower() not in ['content-length', 'connection', 'server']}
                    )
            elif "xml" in content_type:
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    media_type=content_type,
                    headers={k: v for k, v in resp.headers.items() 
                            if k.lower() not in ['content-length', 'connection', 'server']}
                )
            else:
                return Response(
                    content=resp.content,
                    status_code=resp.status_code,
                    media_type=content_type,
                    headers={k: v for k, v in resp.headers.items() 
                            if k.lower() not in ['content-length', 'connection', 'server']}
                )
        except httpx.RequestError as e:
            raise HTTPException(503, f"Service {service} unavailable: {str(e)}")

@app.get("/health")
async def health():
    results = {}
    async with httpx.AsyncClient() as client:
        for name, url in SERVICES.items():
            try:
                resp = await client.get(f"{url}/health", timeout=5)
                results[name] = resp.json()
            except:
                results[name] = {"status": "down"}
    return {"gateway": "ok", "services": results}