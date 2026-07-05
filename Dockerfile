
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

COPY main.py auth.py rate_limiter.py pii_redactor.py monitor.py patterns.json policy.rego ./

EXPOSE 8080

# Cambiamos la llamada al binario por la llamada al módulo de python
RUN useradd -m appuser
USER appuser

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]