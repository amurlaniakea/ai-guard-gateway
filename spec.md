# Functional Specification - AI Guard Gateway

## Requirements

### RQ-1: Security Layer
- **RQ-1.1: Authentication**: Must validate requests via API Key or JWT. Return 401 if invalid.
- **RQ-1.2: Rate Limiting**: Must limit requests per IP to prevent abuse. Return 429 if exceeded.
- **RQ-1.3: Prompt Filtering**: Must block requests containing known injection patterns. Return 403.
- **RQ-1.4: OPA Integration**: Must consult OPA for role-based access. Must FAIL-CLOSED (deny) if OPA is unavailable.
- **RQ-1.5: PII Redaction**: Must mask emails, credit cards, phones, and IPs in backend responses.

### RNF: Non-Functional Requirements
- **RNF-1: Observability**: Must expose a `/metrics` endpoint for Prometheus.
- **RNF-2: Stability**: Must pass all integration tests in the CI pipeline.
