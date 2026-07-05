# Tasks - AI Guard Gateway

## Resumen
Este documento desglosa el plan de implementación (`plan.md`) en una lista de tareas concretas y priorizadas para el proyecto AI Guard Gateway. Cada tarea está asociada a un requisito de la `spec.md` y tiene un estado y una prioridad definidos.

## 1. Configuración Inicial y Prototipo (Fase 1 del Plan)

- [ ] **TAREA-1.1**: Inicializar el repositorio Git en `/home/sil/ai-guard-gateway/`.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `plan.md` (Fase 1)

- [ ] **TAREA-1.2**: Configurar el entorno de desarrollo Python (venv y Poetry).
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `tech-stack.md`, `plan.md` (Fase 1)

- [ ] **TAREA-1.3**: Crear un prototipo básico de proxy inverso con FastAPI.
  - **Descripción**: Un endpoint simple que reenvía solicitudes a un backend de ejemplo.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.1.1, RQ-1.1.2), `plan.md` (Fase 1)

- [ ] **TAREA-1.4**: Implementar pruebas unitarias para el core del proxy.
  - **Descripción**: Asegurar la funcionalidad básica de enrutamiento.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RNF-2.5.2), `plan.md` (Fase 1)

## 2. Inspección de Tráfico y Políticas Básicas (Fase 2 del Plan)

- [ ] **TAREA-2.1**: Desarrollar middleware de inspección de solicitudes/respuestas en FastAPI.
  - **Descripción**: Capturar headers y body de solicitudes/respuestas.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.2.1, RQ-1.2.2, RQ-1.2.3), `plan.md` (Fase 2)

- [ ] **TAREA-2.2**: Integrar Open Policy Agent (OPA) para políticas de seguridad básicas.
  - **Descripción**: Configurar OPA como sidecar o servicio y definir una política Rego simple de denegación.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.5.1, RQ-1.5.2), `plan.md` (Fase 2)

- [ ] **TAREA-2.3**: Implementar detección básica de inyección de prompt.
  - **Descripción**: Usar un conjunto inicial de patrones de palabras clave o expresiones regulares.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.1), `plan.md` (Fase 2)

- [ ] **TAREA-2.4**: Crear pruebas de integración para el middleware de inspección y OPA.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RNF-2.5.2), `plan.md` (Fase 2)

## 3. Detección y Prevención de Ataques Avanzada (Fase 3 del Plan)

- [ ] **TAREA-3.1**: Implementar rate limiting configurable por IP/usuario/endpoint.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.3), `plan.md` (Fase 3)

- [ ] **TAREA-3.2**: Desarrollar módulo de redacción de PII en respuestas de LLM.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.2), `plan.md` (Fase 3)

- [ ] **TAREA-3.3**: Integrar autenticación (JWT/API Keys) y autorización (roles) en el gateway.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.4), `plan.md` (Fase 3)

- [ ] **TAREA-3.4**: Refinar las reglas de detección de inyección de prompt y expandir a otros ataques.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.1), `plan.md` (Fase 3)

- [ ] **TAREA-3.5**: Realizar pruebas de seguridad (ej. fuzzing, ataques de inyección) contra el gateway.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.3.1, RQ-1.3.2, RQ-1.3.3, RQ-1.3.4), `plan.md` (Fase 3)

## 4. Logging y Monitoreo (Fase 4 del Plan)

- [ ] **TAREA-4.1**: Implementar logging estructurado para el gateway.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.4.1), `plan.md` (Fase 4)

- [ ] **TAREA-4.2**: Integrar con Fluentd para la centralización de logs.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RQ-1.4.2), `plan.md` (Fase 4)

- [ ] **TAREA-4.3**: Desarrollar exportador de métricas para Prometheus.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RNF-2.1.1, RNF-2.1.2), `plan.md` (Fase 4)

- [ ] **TAREA-4.4**: Crear dashboard básico en Grafana para visualizar métricas y logs.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `plan.md` (Fase 4)

## 5. Contenerización y Despliegue (Fase 5 del Plan)

- [ ] **TAREA-5.1**: Crear Dockerfile y docker-compose.yml para el gateway y OPA.
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `spec.md` (RNF-2.2.1), `plan.md` (Fase 5)

- [ ] **TAREA-5.2**: Configurar GitHub Actions para CI/CD (pruebas, linting, construcción de imagen).
  - **Prioridad**: Alta
  - **Estado**: Pendiente
  - **Asociado a**: `plan.md` (Fase 5)

- [ ] **TAREA-5.3**: Documentar pasos de despliegue y operación.
  - **Prioridad**: Media
  - **Estado**: Pendiente
  - **Asociado a**: `plan.md` (Fase 5)

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05
