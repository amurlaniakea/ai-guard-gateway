import uvicorn
import httpx
import json
import time 
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from rate_limiter import RateLimiter
from pii_redactor import PIIRedactor
from auth import AuthManager # Importamos el gestor de autenticación

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-guard-gateway.main")

limiter = RateLimiter(requests_limit=5, window_seconds=60)
redactor = PIIRedactor()

class DeepInspectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        if not limiter.is_allowed(client_ip):
            logger.warning(f"[RATE LIMIT BLOCK] IP: {client_ip}")
            return JSONResponse(
                status_code=429, 
                content={"detail": "Too Many Requests - Límite de peticiones superado."}
            )

        req_body = await request.body()
        async def receive():
            return {"type": "http.request", "body": req_body, "more_body": False}
        request._receive = receive

        req_headers = dict(request.headers)
        req_path = request.url.path
        req_method = request.method
        
        logger.info(f"[INCOMING] {req_method} {req_path}")
        if req_body:
            try: body_decoded = req_body.decode("utf-8"); logger.info(f"[INCOMING BODY] {body_decoded[:500]}...")
            except UnicodeDecodeError: logger.info("[INCOMING BODY] Datos binarios")

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        res_body_list = []
        async for chunk in response.body_iterator:
            res_body_list.append(chunk)
        res_body_raw = b''.join(res_body_list)
        
        try:
            res_text = res_body_raw.decode("utf-8")
            redacted_text, count = redactor.redact(res_text)
            if count > 0:
                logger.info(f"[PII REDACTED] Se han eliminado {count} datos sensibles.")
            res_body = redacted_text.encode("utf-8")
        except UnicodeDecodeError:
            res_body = res_body_raw

        logger.info(f"[OUTGOING] Status: {response.status_code} | Duración: {duration:.4f}s")
        
        remaining = limiter.get_remaining(client_ip)
        headers = dict(response.headers)
        headers["X-RateLimit-Limit"] = str(limiter.requests_limit)
        headers["X-RateLimit-Remaining"] = str(remaining)

        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=headers, 
            media_type=response.media_type
        )

def detect_prompt_injection(text: str) -> tuple[bool, str]:
    blacklist = [
        "ignore all previous instructions", "ignore the above instructions",
        "system override", "you are now a", "act as if you are",
        "forget everything", "bypass security", "dan mode", "jailbreak", "malicious"
    ]
    text_lower = text.lower()
    for pattern in blacklist:
        if pattern in text_lower:
            return True, f"Patrón de inyección detectado: {pattern}"
    return False, ""

app = FastAPI(title="AI Guard Gateway - Prototipo con Autenticación")
app.add_middleware(DeepInspectionMiddleware)

OPA_URL = "http://localhost:8181/v1/data/httpapi/authz"

async def check_opa_policy(request: Request, data_to_evaluate: dict) -> tuple[bool, str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPA_URL, json=data_to_evaluate, timeout=1.0)
            response.raise_for_status() 
            result = response.json()
            return result.get("allow", False), "OPA Decision"
    except Exception:
        return None, "OPA unavailable"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_routing(path: str, request: Request):
    # 1. Autenticación y Autorización (TAREA-3.3)
    api_key = request.headers.get("X-API-Key")
    auth_header = request.headers.get("Authorization")
    user_info = None

    if api_key:
        user_info = AuthManager.validate_api_key(api_key)
    elif auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        user_info = AuthManager.validate_jwt(token)
    else:
        raise HTTPException(status_code=401, detail="Falta autenticación. Proporcione X-API-Key o Bearer Token.")

    # Ahora tenemos la identidad del usuario (user_info) que podemos pasar a OPA o usar para cuotas
    logger.info(f"[AUTH] Usuario autenticado: {user_info.get('user')} con rol {user_info.get('role')}")

    # 2. Verificación de Seguridad Nativa
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8") if body_bytes else ""
    prompt_text = body_str
    if body_str and request.headers.get('content-type') == 'application/json':
        try:
            data = json.loads(body_str)
            prompt_text = data.get("prompt") or data.get("content") or body_str
        except json.JSONDecodeError:
            pass
    
    is_malicious, reason = detect_prompt_injection(str(prompt_text))
    if is_malicious:
        logger.warning(f"[SECURITY BLOCK] Prompt malicioso detectado: {reason}")
        raise HTTPException(status_code=403, detail=f"Solicitud bloqueada por seguridad: {reason}")

    # 3. Evaluación OPA (incluyendo la identidad del usuario en el input)
    opa_input = {
        "request": {
            "method": request.method,
            "path": "/" + path, 
            "headers": dict(request.headers),
            "body": json.loads(body_str) if body_str and request.headers.get('content-type') == 'application/json' else body_str,
            "user": user_info # Pasamos la identidad al motor de políticas
        }
    }
    
    opa_allowed, opa_reason = await check_opa_policy(request, opa_input)
    if opa_allowed is False:
        logger.warning(f"[POLICY DENIED] OPA denegó el acceso: {opa_reason}")
        raise HTTPException(status_code=403, detail="Acceso denegado por política de seguridad (OPA).")

    return JSONResponse(
        content={
            "gateway_status": "authorized_and_secure",
            "user": user_info.get("user"),
            "role": user_info.get("role"),
            "target_path": path,
            "method": request.method,
            "security_checks": {
                "native_detection": "passed",
                "opa_evaluation": "allowed" if opa_allowed else "skipped (unavailable)"
            },
            "simulated_llm_response": "Tu solicitud ha sido autenticada, autorizada y procesada."
        },
        status_code=200
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False)
