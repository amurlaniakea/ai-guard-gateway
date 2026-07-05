import uvicorn
import httpx
import json
import time
import logging
import os
import re
import unicodedata
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

# --- LÓGICA DE DETECCIÓN DE INYECCIÓN (Híbrida) ---
try:
    with open("patterns.json", "r") as f:
        PATTERNS = json.load(f)
except Exception:
    PATTERNS = {"nullification_verbs": [], "control_subjects": [], "critical_triggers": []}

def normalize_text(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize('NFKD', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text




def detect_injection(text: str) -> bool:
    normalized = normalize_text(text)
    
    # CAPA 1: Disparadores Críticos (Bloqueo Inmediato)
    if any(trigger in normalized for trigger in PATTERNS.get("critical_triggers", [])):
        return True
    
    # CAPA 2: Intersección Anulación (Verbo Anulación + Sujeto Control)
    has_null_verb = any(v in normalized for v in PATTERNS.get("nullification_verbs", []))
    has_ctrl_subj = any(s in normalized for s in PATTERNS.get("control_subjects", []))
    if has_null_verb and has_ctrl_subj:
        return True
    
    # CAPA 3: Intersección Revelación (Verbo Revelación + Objetivo Info)
    has_rev_verb = any(v in normalized for v in PATTERNS.get("revelation_verbs", []))
    has_info_target = any(s in normalized for s in PATTERNS.get("info_targets", []))
    if has_rev_verb and has_info_target:
        return True
    
    # CAPA 4: Roleplay Malicioso (Inicio Roleplay + (Verbo Anulación o Sujeto Control))
    has_role = any(r in normalized for r in PATTERNS.get("roleplay_starts", []))
    if has_role and (has_null_verb or has_ctrl_subj):
        return True
    
    # CAPA 5: Detección de Ofuscación Extrema
    if len(text) > 10:
        special_chars = len([c for c in text if not c.isalnum() and not c.isspace()])
        if special_chars / len(text) > 0.3:
            return True
            
    return False



    has_verb = any(v in normalized for v in PATTERNS.get("nullification_verbs", []))
    has_subject = any(s in normalized for s in PATTERNS.get("control_subjects", []))
    if has_verb and has_subject:
        return True
    if len(text) > 10:
        special_chars = len([c for c in text if not c.isalnum() and not c.isspace()])
        if special_chars / len(text) > 0.3:
            return True
    return False

# --- MODELOS DE VALIDACIÓN ---
class ChatRequest(BaseModel):
    model: str = Field(..., min_length=1)
    messages: list = Field(...)
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False

# --- DEPENDENCIAS EXTERNAS ---
from auth import validate_auth
from rate_limiter import RateLimiter
from pii_redactor import PIIRedactor

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

        # 2. Inyección de Prompts (Detección Híbrida)
        
        # 2. Inyección de Prompts (Detección sobre CONTENIDO)
        if request.method == "POST":
            try:
                body_bytes = await request.body()
                body_json = json.loads(body_bytes.decode("utf-8"))
                
                # Extraemos todos los contenidos de los mensajes para analizar la inyección
                if "messages" in body_json and isinstance(body_json["messages"], list):
                    all_content = " ".join([m.get("content", "") for m in body_json["messages"] if isinstance(m, dict)])
                    if detect_injection(all_content):
                        log_event("CRITICAL", "prompt_injection_detected", ip=client_ip)
                        return JSONResponse(status_code=403, content={"error": "Security Policy Violation: Prompt Injection Detected"})
                else:
                    # Si no hay mensajes, analizamos el body crudo por si acaso, 
                    # pero el ratio de caracteres especiales ya no disparará falsos positivos masivos
                    body_str = body_bytes.decode("utf-8")
                    if detect_injection(body_str):
                        log_event("CRITICAL", "prompt_injection_detected", ip=client_ip)
                        return JSONResponse(status_code=403, content={"error": "Security Policy Violation: Prompt Injection Detected"})
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
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
                return Response(
                    content=redacted_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
            except Exception as e:
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
    api_key = req_raw.headers.get("X-API-Key")
    auth_header = req_raw.headers.get("Authorization")
    user_info = validate_auth(api_key, auth_header)
    
    if not user_info:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            opa_payload = {"input": {"user": user_info["user"], "role": user_info["role"], "action": "chat"}}
            opa_res = await client.post(OPA_URL, json=opa_payload)
            if opa_res.status_code == 200:
                allowed = opa_res.json().get("result", {}).get("allow", False)
                if not allowed:
                    return JSONResponse(status_code=403, content={"error": "Policy Denied by OPA"})
            else:
                return JSONResponse(status_code=403, content={"error": "Security Governance Error: OPA Server Error"})
    except httpx.HTTPError as e:
        log_event("CRITICAL", "opa_connection_failure", error=str(e))
        return JSONResponse(status_code=403, content={"error": "Security Governance Error: OPA Unavailable"})

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
