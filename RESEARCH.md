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

## 4. Adopción y Escalabilidad
El sistema está diseñado para una adopción rápida mediante:
- **Arquitectura de Proxy**: No requiere cambiar el código del LLM.
- **Configuración Declarativa**: Uso de OPA (Open Policy Agent) para definir reglas de seguridad sin reiniciar el servicio.
- **Baja Latencia**: Optimizado en Python/FastAPI para añadir un overhead insignificante (<10ms).

---
**Documento elaborado por:** Pedro Sordo Martínez (Sil)
**Fecha de fundamento:** 2026-07-05
