# 🛡️ AI Guard Gateway

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/software/free-software-foundation/agpl-3.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)

**AI Guard Gateway** es un proxy inverso de seguridad diseñado específicamente para proteger endpoints de Inteligencia Artificial expuestos. Actúa como un escudo inteligente entre el cliente y el modelo de IA, mitigando riesgos críticos de seguridad y asegurando la privacidad de los datos.

## 🎯 Misión
Proteger la infraestructura de IA contra el abuso y la filtración de datos, implementando capas de defensa proactiva que eviten la inyección de prompts y la exposición de información sensible (PII), manteniendo la baja latencia necesaria para aplicaciones en tiempo real.

Para profundizar en la base científica y la justificación técnica de este proyecto, consulte el archivo [RESEARCH.md](./RESEARCH.md).

## ✨ Características Principales

### 🔒 Seguridad Activa
- **Detección de Inyección de Prompt**: Bloqueo nativo de patrones de ataque comunes (Jailbreaks, System Overrides).
- **Redacción de PII (Privacidad)**: Enmascaramiento automático de emails, tarjetas de crédito e IPs en las respuestas del LLM.
- **Soporte OPA (Open Policy Agent)**: Integración con el estándar de la industria para políticas de seguridad externas y dinámicas.

### 🚦 Control y Gobernanza
- **Rate Limiting Avanzado**: Implementación de Ventana Deslizante (Sliding Window) para prevenir DoS y abuso de cuotas.
- **Autenticación Híbrida**: Soporte para API Keys y JSON Web Tokens (JWT) con gestión de roles.
- **Aislamiento de Identidad**: Trazabilidad completa de quién accede a qué modelo y con qué permisos.

### 📈 Observabilidad Profesional
- **Métricas de Prometheus**: Exposición de contadores de peticiones, bloqueos y latencia en `/metrics`.
- **Logging Estructurado**: Salida de logs en formato JSON compatible con Loki/ELK.
- **Health Checks**: Endpoints de estado para orquestadores como Docker containers.

## 🛠️ Stack Tecnológico
- **Backend**: Python 3.12 + FastAPI
- **Gestión de Dependencias**: Poetry
- **Seguridad**: PyJWT, OPA (Rego)
- **Monitoreo**: Prometheus Client
- **Servidor ASGI**: Uvicorn

## 🚀 Inicio Rápido

### Instalación
```bash
# Clonar el repositorio
git clone https://github.com/amurlaniakea/ai-guard-gateway.git
cd ai-guard-gateway

# Instalar dependencias con Poetry
poetry install
```

### Ejecución
```bash
poetry run python main.py
```
El gateway estará disponible en `http://localhost:8080`.

### Ejemplo de Petición Autorizada
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
     -H "X-API-Key: sk-premium-67890" \
     -H "Content-Type: application/json" \
     -d '{"model": "gpt-4", "messages": [{"role": "user", "content": "Hola"}]}'
```

## ⚖️ Licencia
Este proyecto está bajo la licencia **GNU Affero General Public License v3.0 (AGPL-3.0)**.

## 👤 Autor
**Pedro Sordo Martínez (Sil)** — [amurlaniakea@gmail.com](mailto:amurlaniakea@gmail.com)
