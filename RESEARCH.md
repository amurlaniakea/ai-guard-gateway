# Research & Foundations - AI Guard Gateway

## Theoretical Basis
The AI Guard Gateway is based on the principle of "Defense in Depth". It implements a perimeter security layer to mitigate the "Prompt Injection" attack vector.

## Implementation Logic
Instead of a separate module, the detection logic is integrated directly into the gateway middleware for maximum performance. It uses a set of high-confidence substrings to identify common attack patterns (e.g., "ignore all previous instructions").

## References
- **OWASP Top 10 for LLMs**: Specifically addressing LLM01: Prompt Injection.
- **NIST SP 800-207**: Applying Zero Trust Architecture (ZTA) principles by validating every request via OPA before forwarding it to the backend.
- **Endpoint Hijacking Analysis**: Based on the observation that unprotected endpoints are susceptible to system-prompt overrides.
