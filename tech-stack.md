# Tech Stack - AI Guard Gateway

## Resumen
Este documento describe el stack tecnológico propuesto para el proyecto AI Guard Gateway, enfocado en la seguridad y monitoreo de endpoints de IA expuestos.

## Tecnologías Clave

### Lenguajes de Programación
- **Python**: Lenguaje principal para el desarrollo de la lógica del gateway, análisis de tráfico, integración con LLMs y herramientas de seguridad.
- **JavaScript/TypeScript**: Para el desarrollo de interfaces de usuario (si se requiere un dashboard web) y posibles funciones serverless/edge.

### Frameworks y Librerías

#### Backend (Python)
- **FastAPI**: Para construir la API RESTful del gateway, ofreciendo alto rendimiento y tipado robusto.
- **Pydantic**: Para la validación de datos de entrada/salida en la API.
- **Scapy / dpkt**: Para la inspección de paquetes de red y análisis de tráfico (posiblemente para detección de anomalías).
- **Requests**: Para interactuar con los endpoints de LLM y APIs externas.
- **Ollama / LiteLLM (o similar)**: Para la integración y gestión de diversos modelos de lenguaje.

#### Seguridad y Monitoreo
- **Open Policy Agent (OPA) / Rego**: Para definir y aplicar políticas de autorización y validación en tiempo real.
- **Prometheus / Grafana**: Para la métrica, monitoreo y visualización del rendimiento y seguridad del gateway.
- **Fluentd / ELK Stack**: Para la recolección, agregación y análisis de logs de seguridad.
- **OWASP ModSecurity Core Rule Set (CRS)**: Para la protección contra ataques web comunes a nivel de WAF.
- **YARA**: Para la creación de reglas de detección de patrones maliciosos en payloads de IA.

### Infraestructura y Despliegue
- **Docker / Kubernetes**: Para la contenerización y orquestación del gateway, facilitando la escalabilidad y el despliegue.
- **Nginx / Envoy**: Como proxy inverso y/o sidecar para balanceo de carga, terminación SSL y políticas de tráfico.
- **Git**: Control de versiones.
- **GitHub Actions / GitLab CI/CD**: Para integración y despliegue continuo.

### Bases de Datos (si se requieren)
- **Redis**: Para caching, rate limiting y almacenamiento temporal de sesiones.
- **PostgreSQL**: Para el almacenamiento persistente de configuraciones, logs enriquecidos y datos de auditoría.

### Herramientas de Desarrollo
- **Poetry / Pipenv**: Para la gestión de dependencias de Python.
- **Pytest**: Para testing unitario y de integración.
- **Black / Flake8**: Para formateo y linting de código Python.
- **pre-commit hooks**: Para asegurar la calidad del código antes de cada commit.

## Consideraciones de Seguridad
- **Principio de Mínimo Privilegio**: Todos los componentes se configurarán con los permisos mínimos necesarios.
- **Cifrado en Tránsito y en Reposo**: Asegurar la comunicación y el almacenamiento de datos.
- **Autenticación y Autorización**: Implementación de mecanismos robustos para el acceso al gateway y a sus recursos.
- **Hardening de Contenedores**: Configuración segura de imágenes Docker y entornos de ejecución.

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05
