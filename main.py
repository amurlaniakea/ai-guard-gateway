import uvicorn
import httpx
import json
import time 
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configuración básica de logs
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-guard-gateway.main")

# --- Middleware de Inspección --- 
class DeepInspectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
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
            except UnicodeDecodeError: logger.info("[INCOMING BODY] Datos binarios no decodificables")

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        res_body_list = []
        async for chunk in response.body_iterator:
            res_body_list.append(chunk)
        res_body = b''.join(res_body_list)

        logger.info(f"[OUTGOING] Status: {response.status_code} | Duración: {duration:.4f}s")
        if res_body:
            try: res_decoded = res_body.decode("utf-8"); logger.info(f"[OUTGOING BODY] {res_decoded[:500]}...")
            except UnicodeDecodeError: logger.info("[OUTGOING BODY] Datos binarios de respuesta")

        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=response.headers, 
            media_type=response.media_type
        )

# --- Lógica de Detección de Seguridad (Nativa) --- 
def detect_prompt_injection(text: str) -> tuple[bool, str]:
    """
    Analiza el texto en busca de patrones típicos de inyección de prompts.
    Retorna (is_malicious, reason).
    """
    blacklist = [
        "ignore all previous instructions",
        "ignore the above instructions",
        "system override",
        "you are now a",
        "act as if you are",
        "forget everything",
        "bypass security",
        "dan mode",
        "jailbreak",
        "malicious" # Mantenemos la palabra clave de nuestra política Rego original
    ]
    
    text_lower = text.lower()
    for pattern in blacklist:
        if pattern in text_lower:
            return True, f"Patrón de inyección detectado: {pattern}"
            
    return False, ""

# --- Aplicación FastAPI --- 
app = FastAPI(title="AI Guard Gateway - Prototipo con Seguridad Nativa")
app.add_middleware(DeepInspectionMiddleware)

# URL de OPA (Mantenemos la estructura, pero la desactivamos si no responde)
OPA_URL = "http://localhost:8181/v1/data/httpapi/authz"

async def check_opa_policy(request: Request, data_to_evaluate: dict) -> tuple[bool, str]:
    """Evalúa la política en OPA. Retorna (is_allowed, reason)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OPA_URL, json=data_to_evaluate, timeout=1.0) # Timeout corto
            response.raise_for_status() 
            result = response.json()
            return result.get("allow", False), "OPA Decision"
    except Exception:
        # Si OPA no está disponible, retornamos None para indicar que no pudimos evaluar.
        return None, "OPA unavailable"

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_routing(path: str, request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8") if body_bytes else ""

    # 1. Detección Nativa (T AREA-2.3)
    # Extraemos el prompt si es un JSON
    prompt_text = body_str
    if body_str and request.headers.get('content-type') == 'application/json':
        try:
            data = json.loads(body_str)
            # Buscamos el campo 'prompt' o 'content' comunes en APIs de IA
            prompt_text = data.get("prompt") or data.get("content") or body_str
        except json.JSONDecodeError:
            pass
    
    is_malicious, reason = detect_prompt_injection(str(prompt_text))
    if is_malicious:
        logger.warning(f"[SECURITY BLOCK] Prompt malicioso detectado: {reason}")
        raise HTTPException(status_code=403, detail=f"Solicitud bloqueada por seguridad: {reason}")

    # 2. Evaluación OPA (TAREA-2.2) - Opcional si OPA no está disponible
    opa_input = {
        "request": {
            "method": request.method,
            "path": "/" + path, 
            "headers": dict(request.headers),
            "body": json.loads(body_str) if body_str and request.headers.get('content-type') == 'application/json' else body_str
        }
    }
    
    opa_allowed, opa_reason = await check_opa_policy(request, opa_input)
    if opa_allowed is False: # Solo bloqueamos si OPA responde explícitamente que NO
        logger.warning(f"[POLICY DENIED] OPA denegó el acceso: {opa_reason}")
        raise HTTPException(status_code=403, detail="Acceso denegado por política de seguridad (OPA).")

    # 3. Respuesta final si pasa todos los filtros
    return JSONResponse(
        content={
            "gateway_status": "security_passed",
            "target_path": path,
            "method": request.method,
            "security_checks": {
                "native_detection": "passed",
                "opa_evaluation": "allowed" if opa_allowed else "skipped (unavailable)"
            },
            "simulated_llm_response": "Tu solicitud es segura y ha sido procesada."
        },
        status_code=200
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False)
