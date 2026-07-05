# Roadmap - AI Guard Gateway

## Resumen
Este documento describe la hoja de ruta del proyecto AI Guard Gateway, delineando las fases principales, los hitos clave y los objetivos a corto y largo plazo para asegurar y monitorear endpoints de IA expuestos.

## Fases del Proyecto

### Fase 1: Investigación y Constitución (Actual)
- **Objetivo**: Establecer las bases teóricas y documentales del proyecto.
- **Hitos**: 
  - `mission.md` definido (declaración de misión y visión).
  - `tech-stack.md` definido (selección de tecnologías).
  - `roadmap.md` definido (hoja de ruta inicial).
  - Análisis de nicho y validación de papers completado.
  - Identificación de casos de uso y amenazas clave.

### Fase 2: Diseño de la Especificación Técnica (`spec.md`)
- **Objetivo**: Detallar los requisitos funcionales y no funcionales del gateway.
- **Hitos**:
  - `spec.md` completo con criterios de aceptación claros.
  - Arquitectura de alto nivel definida.
  - Diseño de políticas de seguridad iniciales (Rego).
  - Definición de APIs y contratos de servicio.

### Fase 3: Planificación y Tareas (`plan.md`, `tasks.md`)
- **Objetivo**: Desglosar el diseño en tareas implementables y planificar sprints.
- **Hitos**: 
  - `plan.md` con un plan de implementación detallado.
  - `tasks.md` con una lista de tareas priorizadas y asignadas.
  - Entorno de desarrollo inicial configurado.
  - Pruebas de concepto para componentes clave.

### Fase 4: Implementación (Desarrollo y Pruebas)
- **Objetivo**: Construir el AI Guard Gateway y sus componentes de seguridad.
- **Hitos**: 
  - Desarrollo del core del gateway (FastAPI).
  - Implementación de módulos de inspección de tráfico.
  - Integración con OPA para políticas de seguridad.
  - Desarrollo de módulos de monitoreo y logging (Prometheus, Fluentd).
  - Pruebas unitarias, de integración y de seguridad continuas.
  - Refactorización y optimización del código.

### Fase 5: Despliegue y Operaciones
- **Objetivo**: Poner el gateway en producción y asegurar su operación continua.
- **Hitos**: 
  - Contenerización y orquestación con Docker/Kubernetes.
  - Configuración de CI/CD para despliegues automatizados.
  - Establecimiento de dashboards de monitoreo (Grafana).
  - Implementación de alertas de seguridad.
  - Documentación operativa y manuales de usuario.
  - Auditorías de seguridad post-despliegue.

## Objetivos a Largo Plazo
- **Adaptabilidad a Nuevas Amenazas**: Evolucionar el gateway para contrarrestar nuevas técnicas de ataque en el ámbito de la IA.
- **Integración con Ecosistemas de Seguridad Existentes**: Compatibilidad con SIEMs, SOARs y otras plataformas de seguridad.
- **Aprendizaje Continuo**: Incorporar capacidades de ML para la detección autónoma de anomalías y ataques.
- **Código Abierto y Comunidad**: Fomentar la colaboración y contribución de la comunidad.

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05
