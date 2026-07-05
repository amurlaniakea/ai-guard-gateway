
from prometheus_client import Counter, Histogram

# Métricas de Prometheus
REQUESTS_TOTAL = Counter(
    'gateway_requests_total', 
    'Total number of requests processed by the gateway',
    ['method', 'endpoint', 'status']
)

REQUESTS_BLOCKED_TOTAL = Counter(
    'gateway_requests_blocked_total', 
    'Total number of requests blocked by security policies',
    ['reason']
)

REQUEST_DURATION = Histogram(
    'gateway_request_duration_seconds', 
    'Duration of requests in seconds',
    ['endpoint']
)
