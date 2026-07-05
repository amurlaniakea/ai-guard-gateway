# Project Roadmap - AI Guard Gateway

## Current State: v0.1.0 (Perimeter Protection)
- Basic pattern-based filtering.
- OPA-based identity governance (Fail-Closed).
- IP-based rate limiting.
- PII redaction for 5 core patterns.

## Short Term Goals (v0.2.0)
- **Pattern Expansion**: Implement support for Spanish and other common languages.
- **Pattern Management**: Move hardcoded patterns to a JSON configuration file or a lightweight DB (SQLite).
- **Enhanced OPA Policies**: Implement more granular role-based access control.

## Long Term Vision
- **Semantic Analysis**: Explore the integration of small LLMs to detect prompt injection intent instead of just substrings.
- **Enterprise Integration**: Support for standard OAuth2/OIDC providers.
