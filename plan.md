# Plan - AI Guard Gateway

## Resumen
Este documento describe el plan de implementación detallado para el proyecto AI Guard Gateway, desglosando las fases de desarrollo en tareas manejables y asignando prioridades. Este plan sigue la `spec.md` y la `tech-stack.md` para asegurar una implementación coherente y efectiva.

## 1. Plan General por Fases

### Fase 1: Configuración Inicial y Prototipo (1 semana)
- **Objetivo**: Establecer el entorno de desarrollo y validar la estructura básica del proxy.
- **Hitos**: 
  - Configuración de un repositorio git y entorno de desarrollo (venv, poetry).
  - Prototipo básico de proxy inverso con FastAPI y enrutamiento simple.
  - Pruebas unitarias iniciales para el core del proxy.

### Fase 2: Implementación de Inspección de Tráfico y Políticas Básicas (2 semanas)
- **Objetivo**: Habilitar la inspección de payloads y la aplicación de políticas de seguridad iniciales.
- **Hitos**: 
  - Middleware para la inspección de solicitudes/respuestas en FastAPI.
  - Integración básica con OPA (Open Policy Agent) para una política de denegación simple.
  - Detección básica de inyección de prompt (ej. patrones de palabras clave).
  - Pruebas de integración para la inspección y políticas.

### Fase 3: Detección y Prevención de Ataques Avanzada (3 semanas)
- **Objetivo**: Fortalecer las capacidades de seguridad del gateway con mecanismos de detección y prevención avanzados.
- **Hitos**: 
  - Implementación de rate limiting configurable.
  - Módulo de redacción de PII en respuestas (ej. expresiones regulares).
  - Mecanismos de autenticación y autorización (ej. JWT, API Keys) para el acceso al gateway.
  - Refinamiento de las reglas de detección de inyección de prompt y otros ataques.
  - Pruebas de seguridad (pen-testing básico) para las vulnerabilidades cubiertas.

### Fase 4: Logging y Monitoreo (2 semanas)
- **Objetivo**: Establecer una infraestructura robusta para la auditoría y monitoreo del gateway.
- **Hitos**: 
  - Implementación de logging estructurado (JSON) para todas las solicitudes/respuestas.
  - Integración con Fluentd para la centralización de logs.
  - Exportador de métricas para Prometheus (latencia, QPS, bloqueos).
  - Dashboard básico en Grafana para visualizar métricas y logs.

### Fase 5: Contenerización y Despliegue (1 semana)
- **Objetivo**: Preparar el gateway para el despliegue en entornos de producción.
- **Hitos**: 
  - Archivos Dockerfile y docker-compose.yml para el gateway y OPA.
  - Configuración de GitHub Actions para CI/CD (pruebas, linting, construcción de imagen).
  - Documentación de despliegue y operación.

## 2. Dependencias Críticas
- **FastAPI**: Core del gateway.
- **OPA**: Motor de políticas de seguridad.
- **Docker/Kubernetes**: Entorno de despliegue.
- **Prometheus/Grafana**: Monitoreo.

## 3. Riesgos Potenciales
- **Complejidad de las reglas de OPA**: Curva de aprendizaje y mantenimiento.
- **Falsos positivos/negativos**: Equilibrio entre seguridad y usabilidad.
- **Impacto en el rendimiento**: La inspección profunda podría introducir latencia.
- **Evolución rápida de amenazas de IA**: Necesidad de actualizaciones constantes.

## 4. Estrategia de Pruebas
- **Unitarias**: Para cada función y clase (80% de cobertura mínima).
- **Integración**: Para las interacciones entre componentes (proxy, OPA, logging).
- **Seguridad**: Pruebas de inyección, exposición de datos, denegación de servicio.
- **Rendimiento**: Benchmarking con herramientas como `wrk` o `locust`.

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05
