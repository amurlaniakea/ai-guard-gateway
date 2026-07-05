import uvicorn
import httpx
import json
import time 
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from rate_limiter import RateLimiter
from pii_redactor import PIIRedactor
from auth import AuthManager
from monitor import REQUESTS_TOTAL, REQUESTS_BLOCKED_TOTAL, REQUEST_DURATION
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-guard-gateway.main")

limiter = RateLimiter(requests_limit=5, window_seconds=60)
redactor = PIIRedactor()

class DeepInspectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # EXCLUSIÓN DE RUTAS INTERNAS: No aplicar middleware a métricas y salud
        if request.url.path in ["/metrics", "/health"]:
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "unknown"
        
        if not limiter.is_allowed(client_ip):
            REQUESTS_BLOCKED_TOTAL.labels(reason="rate_limit").inc()
            log_event("WARN", "rate_limit_blocked", ip=client_ip)
            return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

        req_body = await request.body()
        async def receive():
            return {"type": "http.request", "body": req_body, "more_body": False}
        request._receive = receive

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        endpoint = request.url.path
        REQUESTS_TOTAL.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        REQUEST_DURATION.labels(endpoint=endpoint).observe(duration)

        res_body_list = []
        async for chunk in response.body_iterator:
            res_body_list.append(chunk)
        res_body_raw = b''.join(res_body_list)
        
        try:
            res_text = res_body_raw.decode("utf-8")
            redacted_text, count = redactor.redact(res_text)
            if count > 0:
                log_event("INFO", "pii_redacted", count=count)
            res_body = redacted_text.encode("utf-8")
        except UnicodeDecodeError:
            res_body = res_body_raw

        remaining = limiter.get_remaining(client_ip)
        headers = dict(response.headers)
        headers["X-RateLimit-Remaining"] = str(remaining)

        return Response(content=res_body, status_code=response.status_code, headers=headers, media_type=response.media_type)

def log_event(level, event, **kwargs):
    log_entry = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "level": level, "event": event, **kwargs}
    print(json.dumps(log_entry))

def detect_prompt_injection(text: str) -> tuple[bool, str]:
    blacklist = ["ignore all previous instructions", "system override", "jailbreak", "malicious"]
    text_lower = text.lower()
    for pattern in blacklist:
        if pattern in text_lower:
            return True, pattern
    return False, ""

app = FastAPI(title="AI Guard Gateway - Final Monitoring")
app.add_middleware(DeepInspectionMiddleware)

OPA_URL = "http://localhost:8181/v1/data/httpapi/authz"

async def check_opa_policy(request: Request, data_to_evaluate: dict) -> tuple[bool, str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPA_URL, json=data_to_evaluate, timeout=1.0)
            response.raise_for_status() 
            return response.json().get("allow", False), "OPA Decision"
    except Exception:
        return None, "OPA unavailable"

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_routing(path: str, request: Request):
    # Excluir rutas internas de la autenticación
    if path in ["health", "metrics"]:
        user_info = {"user": "system", "role": "system"}
    else:
        api_key = request.headers.get("X-API-Key")
        auth_header = request.headers.get("Authorization")
        user_info = None

        if api_key: user_info = AuthManager.validate_api_key(api_key)
        elif auth_header and auth_header.startswith("Bearer "):
            user_info = AuthManager.validate_jwt(auth_header.split(" ")[1])
        else:
            REQUESTS_BLOCKED_TOTAL.labels(reason="auth_missing").inc()
            raise HTTPException(status_code=401, detail="Falta autenticación.")

    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8") if body_bytes else ""
    
    prompt_text = body_str
    if body_str and request.headers.get('content-type') == 'application/json':
        try:
            data = json.loads(body_str)
            prompt_text = data.get("prompt") or data.get("content") or body_str
        except json.JSONDecodeError: pass
    
    is_malicious, reason = detect_prompt_injection(str(prompt_text))
    if is_malicious:
        REQUESTS_BLOCKED_TOTAL.labels(reason="injection").inc()
        log_event("WARN", "injection_blocked", reason=reason, user=user_info.get("user"))
        raise HTTPException(status_code=403, detail=f"Bloqueado: {reason}")

    opa_allowed, _ = await check_opa_policy(request, {"request": {"body": body_str}})
    if opa_allowed is False:
        REQUESTS_BLOCKED_TOTAL.labels(reason="opa_policy").inc()
        log_event("WARN", "opa_blocked", user=user_info.get("user"))
        raise HTTPException(status_code=403, detail="Denegado por OPA.")

    return JSONResponse(content={"status": "secure", "user": user_info.get("user")}, status_code=200)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False)
