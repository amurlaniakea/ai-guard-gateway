# 🔬 Research & Fundamentals - AI Guard Gateway

## 1. Justificación de la Creación
La proliferación de modelos de lenguaje locales (Local LLMs) y la democratización de la inferencia mediante herramientas como **Ollama, LiteLLM y vLLM** han creado un nuevo vector de ataque: **AI Endpoint Hijacking**.

Muchos administradores despliegan estos servicios en entornos de nube o redes internas sin capas de seguridad, exponiendo el puerto de la API directamente. Esto permite que atacantes externos realicen:
- **Resource Exhaustion**: Agotar la GPU del servidor mediante peticiones masivas.
- **Prompt Injection**: Manipular el modelo para saltar restricciones de seguridad.
- **Data Exfiltration**: Forzar al modelo a revelar datos sensibles del sistema o del contexto.

**AI Guard Gateway** nace para resolver este problema proporcionando una capa de seguridad "Plug-and-Play" que no requiere modificar el modelo, sino proteger la comunicación.

## 2. Fundamentos y Fuentes Científicas
El diseño de este gateway se basa en el análisis de vulnerabilidades reales observadas en la infraestructura de IA moderna:

### 2.1. Análisis de Endpoints Expuestos
Se ha documentado que una cantidad significativa de endpoints de IA están expuestos sin autenticación. El análisis de fuentes técnicas (como reportes de Dev.to y auditorías de seguridad en GitHub) indica que los atacantes utilizan escaneos de puertos para encontrar instancias de Ollama y ejecutar operaciones ofensivas sin necesidad de exploits complejos, simplemente aprovechando la falta de control de acceso.

### 2.2. El problema de la "Confianza Implícita"
La mayoría de los frameworks de inferencia asumen que si una petición llega al puerto, es legítima. El AI Guard Gateway rompe este paradigma implementando la filosofía de **Zero Trust** aplicada a la IA.

## 3. Estrategia de Mitigación implementada
Para combatir las amenazas identificadas, el proyecto implementa tres pilares:
1. **Validación de Identidad**: Implementación de API Keys y JWT para eliminar la exposición anónima.
2. **Saneamiento de Entrada**: Detección nativa de patrones de inyección de prompts basados en el análisis de comportamiento de LLMs.
3. **Control de Salida**: Redacción de PII para evitar que el modelo actúe como un oráculo de datos sensibles.

## 4. Referencias y Fuentes Consultadas

Para la construcción de este gateway se han analizado las siguientes fuentes y marcos de trabajo:

### 4.1. Fuentes Técnicas y Reportes de Vulnerabilidad
- **Análisis de Secuestro de Endpoints**: [*"Attackers are hijacking exposed AI endpoints to run offensive operations - no exploit needed"*](https://dev.to/cyclopt_dimitrisk/attackers-are-hijacking-exposed-ai-endpoints-to-run-offensive-operations-no-exploit-needed-123d) (Dev.to). Este análisis fue la señal clave para validar la necesidad de un gateway que bloquee el acceso anónimo a instancias de Ollama y LiteLLM.
- **Auditorías de Seguridad de GitHub**: Análisis de repositorios de inferencia local para identificar la falta de capas de autenticación por defecto en despliegues de producción.

### 4.2. Marcos de Trabajo (Frameworks)
- **[OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**: El proyecto implementa mitigaciones directas para las vulnerabilidades listadas por OWASP, específicamente:
    - *LLM01: Prompt Injection* $\rightarrow$ Mitigado mediante el módulo `detect_prompt_injection`.
    - *LLM06: Sensitive Information Disclosure* $\rightarrow$ Mitigado mediante el `PIIRedactor`.
- **[NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final)**: Aplicación del principio de "nunca confiar, siempre verificar" mediante la obligatoriedad de JWT/API Keys antes de cualquier procesamiento de datos.

---
**Documento elaborado por:** Pedro Sordo Martínez (Sil)
**Fecha de fundamento:** 2026-07-05
