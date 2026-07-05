

import json
import re
import unicodedata

try:
    with open("patterns.json", "r") as f:
        PATTERNS = json.load(f)
except Exception:
    PATTERNS = {"nullification_verbs": [], "control_subjects": [], "roleplay_triggers": []}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_injection(text: str) -> bool:
    normalized = normalize_text(text)
    has_verb = any(v in normalized for v in PATTERNS["nullification_verbs"])
    has_subject = any(s in normalized for s in PATTERNS["control_subjects"])
    if has_verb and has_subject:
        return True
    if any(r in normalized for r in PATTERNS["roleplay_triggers"]):
        return True
    return False


import uvicorn
import httpx
import json
import time
import logging
import os
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field

# --- CONFIGURACIÓN Y LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-guard-gateway")

OPA_URL = os.getenv("OPA_URL", "http://localhost:8181/v1/data/httpapi/authz")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:11434")

def log_event(level: str, event: str, **kwargs):
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "event": event,
        **kwargs
    }
    logger.info(json.dumps(log_entry))

# --- MODELOS DE VALIDACIÓN (Anti-Injection) ---
class ChatRequest(BaseModel):
    model: str = Field(..., min_length=1)
    messages: list = Field(...)
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False

# --- LÓGICA DE SEGURIDAD (Importada) ---
from auth import validate_auth
from rate_limiter import RateLimiter
from pii_redactor import PIIRedactor


import json
import re
import unicodedata

# Carga de patrones al iniciar
try:
    with open("patterns.json", "r") as f:
        INJECTION_PATTERNS = json.load(f)
except Exception:
    INJECTION_PATTERNS = {"english": [], "spanish": []}

def normalize_text(text: str) -> str:
    """Normaliza el texto para derrotar ofuscaciones simples."""
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

    """Detecta inyecciones comparando texto normalizado contra patrones."""
    normalized = normalize_text(text)
    all_patterns = INJECTION_PATTERNS["english"] + INJECTION_PATTERNS["spanish"]
    for p in all_patterns:
        if normalize_text(p) in normalized:
            return True
    return False


limiter = RateLimiter(max_requests=5, window_seconds=60)
redactor = PIIRedactor()

# --- MIDDLEWARE DE INSPECCIÓN PROFUNDA ---
class DeepInspectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/metrics", "/health"]:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        
        # 1. Rate Limiting
        if not limiter.allow_request(client_ip):
            log_event("WARN", "rate_limit_exceeded", ip=client_ip)
            return JSONResponse(status_code=429, content={"error": "Too Many Requests"})

        # 2. Inyección de Prompts (Detección Nativa)
        if request.method == "POST":
            try:
                body = await request.body()
                body_str = body.decode("utf-8")
                forbidden_patterns = ["ignore all previous instructions", "system override", "you are now a"]
                if any(p in body_str.lower() for p in forbidden_patterns):
                    log_event("CRITICAL", "prompt_injection_detected", ip=client_ip)
                    return JSONResponse(status_code=403, content={"error": "Security Policy Violation: Prompt Injection Detected"})
            except UnicodeDecodeError as e:
                log_event("ERROR", "body_read_failure", error=str(e))
                return JSONResponse(status_code=400, content={"error": "Invalid request body"})

        response = await call_next(request)
        
        # 3. Redacción de PII en la respuesta
        if response.status_code == 200:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            try:
                decoded_body = response_body.decode("utf-8")
                redacted_body = redactor.redact(decoded_body)
                # Devolvemos una nueva respuesta para evitar problemas de Content-Length
                return Response(
                    content=redacted_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
            except (ValueError, TypeError, AttributeError) as e:
                log_event("ERROR", "pii_redaction_failure", error=str(e))
                return Response(content=response_body, status_code=response.status_code)

        return response

app = FastAPI(title="AI Guard Gateway")
app.add_middleware(DeepInspectionMiddleware)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/metrics")
async def metrics():
    from monitor import generate_latest_metrics
    return Response(content=generate_latest_metrics(), media_type="text/plain")


@app.post("/v1/chat/completions")
async def proxy_chat(request: ChatRequest, req_raw: Request):
    # 1. Autenticación
    api_key = req_raw.headers.get("X-API-Key")
    auth_header = req_raw.headers.get("Authorization")
    user_info = validate_auth(api_key, auth_header)
    
    if not user_info:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    # 2. Gobernanza OPA (Sincronizada - FAIL CLOSED)
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            opa_payload = {"input": {"user": user_info["user"], "role": user_info["role"], "action": "chat"}}
            opa_res = await client.post(OPA_URL, json=opa_payload)
            if opa_res.status_code == 200:
                allowed = opa_res.json().get("result", {}).get("allow", False)
                if not allowed:
                    return JSONResponse(status_code=403, content={"error": "Policy Denied by OPA"})
            else:
                # Fail-Closed: Si OPA devuelve error HTTP, denegamos
                return JSONResponse(status_code=403, content={"error": "Security Governance Error: OPA Server Error"})
    except httpx.HTTPError as e:
        log_event("CRITICAL", "opa_connection_failure", error=str(e))
        return JSONResponse(status_code=403, content={"error": "Security Governance Error: OPA Unavailable"})

    # 3. Forwarding al Backend (Llamada Segura)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            backend_res = await client.post(
                f"{BACKEND_URL}/v1/chat/completions",
                json=request.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            return Response(
                content=backend_res.content,
                status_code=backend_res.status_code,
                headers=dict(backend_res.headers)
            )
    except httpx.HTTPError as e:
        log_event("ERROR", "backend_failure", error=str(e))
        return JSONResponse(status_code=502, content={"error": "Bad Gateway"})
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
