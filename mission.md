# AI-Guard-Gateway - Mission Statement

## Visión
Crear un proxy ligero de seguridad en runtime que proteja endpoints expuestos de Ollama y LiteLLM contra ataques de secuestro de compute para operaciones ofensivas, mediante inspección semántica de payloads de agentes.

## Misión
Proteger la infraestructura AI self-hosted contra el secuestro de compute mediante un gateway de seguridad que inspeccione los payloads completos de los agentes (system prompts, tool definitions, personas) para detectar tooling ofensivo conocido y patrones de evasión de seguridad.

## Por qué
- Los endpoints de Ollama (puerto 11434) y LiteLLM (sin auth o clave por defecto) están siendo secuestrados para operaciones ofensivas sin necesidad de exploits
- 3 campañas reales documentadas por Zenity (Mar-May 2026) usando Strix, HexStrike y otras herramientas
- No existe una herramienta open-source ligera que inspeccione semánticamente los payloads de agentes
- Es el "mismo patrón que S3 buckets abiertos" pero con AI compute

## Para quién
- Equipos que despliegan Ollama/LiteLLM en producción
- Organizaciones que usan agentes de IA con infraestructura self-hosted
- Cualquiera con endpoints expuestos de modelos locales

## Cómo
- Proxy ligero plug-and-play delante de Ollama/LiteLLM
- Inspección semántica de payloads (system prompts, tools, personas)
- Base de datos extensible de tooling ofensivo conocido
- Sistema de scoring ponderado y umbrales configurables
- Logging estructurado y alertas

## Éxito significa
- Bloquear requests con payloads ofensivos conocidos (Strix, HexStrike, etc.)
- Detectar patrones de evasión de seguridad en system prompts
- Mantener latencia <10ms overhead
- Fácil integración con infraestructura existente
- 0 falsos positivos críticos en entornos de prueba

---
**Autor:** Pedro Sordo Martínez (Sil) — amurlaniakea@gmail.com
**Licencia:** AGPL-3.0-or-later
**Fecha:** 2026-07-05