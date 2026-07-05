import time
from collections import defaultdict, deque
from threading import Lock

class RateLimiter:
    """
    Implementación de Rate Limiting mediante Ventana Deslizante (Sliding Window).
    Controla el número de solicitudes permitidas por cliente en un intervalo de tiempo.
    """
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # Diccionario donde la llave es el cliente (IP) y el valor es una cola de timestamps de sus peticiones
        self.client_requests = defaultdict(deque)
        self.lock = Lock() # Aseguramos que el acceso sea thread-safe

    def is_allowed(self, client_id: str) -> bool:
        with self.lock:
            now = time.time()
            requests = self.client_requests[client_id]
            
            # 1. Limpiar timestamps antiguos que ya están fuera de la ventana actual
            while requests and requests[0] <= now - self.window_seconds:
                requests.popleft()
            
            # 2. Verificar si el cliente ha superado el límite
            if len(requests) < self.requests_limit:
                requests.append(now)
                return True
            
            return False

    def get_remaining(self, client_id: str) -> int:
        """Devuelve cuántas peticiones le quedan al cliente en la ventana actual."""
        with self.lock:
            now = time.time()
            requests = self.client_requests[client_id]
            while requests and requests[0] <= now - self.window_seconds:
                requests.popleft()
            return max(0, self.requests_limit - len(requests))
