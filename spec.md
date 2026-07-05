# Spec - AI Guard Gateway

## Resumen
Este documento detalla la especificación técnica (Spec) para el proyecto AI Guard Gateway. Define los requisitos funcionales y no funcionales, la arquitectura propuesta, los componentes clave y los criterios de aceptación para cada característica, asegurando que el desarrollo cumpla con los estándares de seguridad y rendimiento.

## 1. Requisitos Funcionales

### 1.1 Proxy y Enrutamiento de Tráfico
- **RQ-1.1.1**: El gateway debe actuar como un proxy inverso para solicitudes HTTP/HTTPS dirigidas a endpoints de IA (LLMs, modelos de visión, etc.).
- **RQ-1.1.2**: Debe ser capaz de enrutar solicitudes a múltiples backends de IA basados en reglas configurables (e.g., path, headers, query params).
- **RQ-1.1.3**: Debe soportar la terminación SSL/TLS y la re-encriptación hacia los backends.

### 1.2 Inspección de Solicitudes y Respuestas (Payloads de IA)
- **RQ-1.2.1**: Debe interceptar y analizar payloads de solicitudes HTTP/HTTPS (headers, body) antes de reenviarlas al backend de IA.
- **RQ-1.2.2**: Debe interceptar y analizar payloads de respuestas HTTP/HTTPS antes de reenviarlas al cliente.
- **RQ-1.2.3**: La inspección debe ser configurable para diferentes tipos de contenido (JSON, texto plano, etc.).

### 1.3 Detección y Prevención de Ataques (OWASP Top 10 para LLMs)
- **RQ-1.3.1 (Inyección de Prompt)**: Debe detectar y mitigar intentos de inyección de prompt directo/indirecto en las solicitudes.
  - **Criterio de Aceptación (CA)**: El gateway bloquea el 95% de los ataques de inyección de prompt conocidos sin falsos positivos críticos.
- **RQ-1.3.2 (Exposición de Datos Sensibles)**: Debe prevenir la exposición de datos sensibles en las respuestas del LLM.
  - **CA**: El gateway redacta o bloquea el 100% de la información personal identificable (PII) configurada en las respuestas.
- **RQ-1.3.3 (Denegación de Servicio)**: Debe implementar rate limiting y otras medidas para prevenir ataques de denegación de servicio.
  - **CA**: El gateway soporta 1000 QPS con una latencia < 50ms antes de activar el rate limiting.
- **RQ-1.3.4 (Acceso No Autorizado)**: Debe aplicar políticas de autorización basadas en roles o atributos para el acceso a endpoints de IA.
  - **CA**: El gateway rechaza el 100% de las solicitudes de usuarios no autorizados a recursos protegidos.

### 1.4 Auditoría y Logging
- **RQ-1.4.1**: Debe registrar todas las solicitudes y respuestas procesadas, incluyendo metadatos relevantes para la seguridad.
- **RQ-1.4.2**: Los logs deben ser exportables a sistemas externos (SIEM, Fluentd) en formatos estándar (JSON).
- **RQ-1.4.3**: Debe registrar eventos de seguridad (bloqueos, alertas) con detalles suficientes para una investigación.

### 1.5 Gestión de Políticas
- **RQ-1.5.1**: Debe permitir la definición de políticas de seguridad dinámicas (e.g., usando Rego/OPA).
- **RQ-1.5.2**: Las políticas deben poder actualizarse sin reiniciar el gateway.

## 2. Requisitos No Funcionales

### 2.1 Rendimiento
- **RNF-2.1.1**: **Latencia**: El gateway no debe añadir más de 10ms de latencia promedio al tráfico normal.
- **RNF-2.1.2**: **Throughput**: Debe ser capaz de manejar al menos 5000 QPS (consultas por segundo) para payloads típicos.

### 2.2 Escalabilidad
- **RNF-2.2.1**: Debe ser escalable horizontalmente (mediante Docker/Kubernetes) para manejar picos de carga.

### 2.3 Fiabilidad y Resiliencia
- **RNF-2.3.1**: Debe ser altamente disponible (99.99% de uptime).
- **RNF-2.3.2**: Debe implementar mecanismos de reintento y circuit breaker para las conexiones a backends de IA.

### 2.4 Seguridad (del propio Gateway)
- **RNF-2.4.1**: El gateway debe adherirse a los principios de seguridad por diseño (secure by design).
- **RNF-2.4.2**: Todas las dependencias deben ser escaneadas regularmente en busca de vulnerabilidades.
- **RNF-2.4.3**: Las credenciales y configuraciones sensibles deben gestionarse de forma segura (e.g., HashiCorp Vault, Kubernetes Secrets).

### 2.5 Mantenibilidad
- **RNF-2.5.1**: El código debe ser modular, legible y estar bien documentado.
- **RNF-2.5.2**: Debe contar con una cobertura de pruebas mínima del 80% (unitarias e integración).

## 3. Arquitectura de Alto Nivel
(Se detallará en un documento `architecture.md` posterior o como parte de la sección de diseño)

## 4. Componentes Clave
- **Core Proxy**: Basado en FastAPI.
- **Módulo de Inspección**: Scapy/dpkt o middleware personalizado.
- **Motor de Políticas**: Open Policy Agent (OPA) con reglas Rego.
- **Módulo de Logging**: Integración con Fluentd.
- **Módulo de Monitoreo**: Exportador de métricas para Prometheus.

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05
