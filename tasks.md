# Project Tasks - AI Guard Gateway

## Phase 1: Core Infrastructure [COMPLETED]
- [x] TAREA-1.1: Initialize Git Repository and Poetry environment.
- [x] TAREA-1.2: Implement basic FastAPI Proxy structure.
- [x] TAREA-1.3: Setup basic logging and health checks.

## Phase 2: Security Modules [COMPLETED]
- [x] TAREA-2.1: Implement API Key and JWT Authentication.
- [x] TAREA-2.2: Implement IP-based Rate Limiting.
- [x] TAREA-2.3: Implement PII Redactor (Email, Card, Phone, IP, SSN).
- [x] TAREA-2.4: Implement Prompt Injection filter (Pattern-based).
- [x] TAREA-2.5: Integrate OPA with Fail-Closed logic.

## Phase 3: Observability and CI/CD [COMPLETED]
- [x] TAREA-3.1: Implement Prometheus metrics endpoint.
- [x] TAREA-3.2: Configure SonarCloud analysis.
- [x] TAREA-3.3: Implement Pytest suite and CI job in GitHub Actions.

## Phase 4: Hardening and Production (PENDING)
- [ ] TAREA-4.1: Hardening de Inyección (Umbral: >=85% Bloqueo / <=5% Falsos Positivos)
- [ ] TAREA-4.2: Implement a proper database for PII patterns and blacklist.
- [ ] TAREA-4.3: Optimize latency for high-traffic scenarios.

- [ ] TAREA-4.4: Detección de ataques codificados (Base64, hex, ROT13) y ataques en idiomas
      distintos de ES/EN. El detector actual normaliza texto plano pero no decodifica payloads
      codificados ni cubre patrones fuera de español/inglés.