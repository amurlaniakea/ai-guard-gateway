# Project Mission - AI Guard Gateway

## Vision
To provide a transparent, low-latency security layer that protects AI endpoints from common prompt injection attacks and ensures identity governance.

## Current Scope (v0.1.0)
The AI Guard Gateway acts as a first-line defense (Perimeter Protection) focused on:
- **Pattern-Based Filtering**: Blocking known prompt injection signatures (e.g., "ignore all previous instructions").
- **Identity Governance**: Enforcing access control policies via OPA (Open Policy Agent).
- **Traffic Control**: Preventing API abuse through IP-based rate limiting.
- **Data Privacy**: Redacting sensitive PII (emails, cards, phones, IPs) from responses before they reach the client.

## Goals
- Provide a "fail-closed" security posture.
- Maintain minimal latency overhead.
- Ensure full observability of blocked requests via Prometheus metrics.
