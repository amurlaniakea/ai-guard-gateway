import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configuración básica de logs para ver la interceptación en tiempo real
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-guard-gateway.middleware")

class DeepInspectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. INSPECCIÓN DE LA SOLICITUD (REQUEST)
        # Leemos el cuerpo crudo de la solicitud
        req_body = await request.body()
        
        # Truco técnico esencial: Re-inyectamos el body en el canal de recepción
        # para que FastAPI/Uvicorn puedan volver a leerlo en las rutas sin colgarse.
        async def receive():
            return {"type": "http.request", "body": req_body, "more_body": False}
        request._receive = receive

        req_headers = dict(request.headers)
        req_path = request.url.path
        req_method = request.method

        logger.info(f"[INCOMING] {req_method} {req_path} | Headers: {list(req_headers.keys())}")
        if req_body:
            # Intentamos decodificar a texto legible para los logs de auditoría
            try:
                body_decoded = req_body.decode("utf-8")
                logger.info(f"[INCOMING BODY] {body_decoded[:500]}...")  # Limitamos log a 500 chars
            except UnicodeDecodeError:
                logger.info("[INCOMING BODY] Datos binarios no decodificables")

        # 2. SEGUIR LA CADENA DE EJECUCIÓN
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # 3. INSPECCIÓN DE LA RESPUESTA (RESPONSE)
        # Consumimos el iterador del cuerpo de la respuesta de forma segura
        res_body = b""
        async for chunk in response.body_iterator:
            res_body += chunk

        logger.info(f"[OUTGOING] Status: {response.status_code} | Duración: {duration:.4f}s")
        if res_body:
            try:
                res_decoded = res_body.decode("utf-8")
                logger.info(f"[OUTGOING BODY] {res_decoded[:500]}...")
            except UnicodeDecodeError:
                logger.info("[OUTGOING BODY] Datos binarios de respuesta")

        # Re-empaquetamos el cuerpo de la respuesta consumida para que el cliente la reciba intacta
        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )
