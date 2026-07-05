# Technical Stack - AI Guard Gateway

This project implements a lightweight security proxy for AI endpoints.

## Core Stack
- **Language**: Python 3.12
- **Framework**: FastAPI (Asynchronous ASGI)
- **Dependency Management**: Poetry
- **Security Engine**: Open Policy Agent (OPA) via REST API
- **Observability**: Prometheus (Client library for metrics)
- **Authentication**: JWT (PyJWT) & Static API Keys
- **Logging**: Structured JSON Logging

## Infrastructure (Local/Dev)
- **Containerization**: Docker (Target)
- **CI/CD**: GitHub Actions
- **Static Analysis**: SonarCloud, Bandit, Flake8
