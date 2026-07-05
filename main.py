import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from middleware import DeepInspectionMiddleware

app = FastAPI(title="AI Guard Gateway - Prototipo con Middleware")

# Registramos el middleware de inspección profunda
app.add_middleware(DeepInspectionMiddleware)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_routing(path: str, request: Request):
    # Gracias a la inyección del canal en middleware.py, 
    # podemos leer request.body() aquí sin problemas ni cuelgues.
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8") if body_bytes else ""
    
    return JSONResponse(
        content={
            "gateway_status": "inspected_and_passed",
            "target_path": path,
            "method": request.method,
            "body_received": body_str,
            "simulated_llm_response": "Este endpoint ha pasado por la inspección profunda de seguridad."
        },
        status_code=200
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
