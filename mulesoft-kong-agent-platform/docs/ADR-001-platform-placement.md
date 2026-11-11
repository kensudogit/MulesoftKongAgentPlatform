# ADR-001: MuleSoft × Kong × FastAPI placement for AI-Agent APIs

## Status
Proposed (local demo validated; production inputs pending)

## Context
Enterprise AI agents need governed API access with edge policy, transformation/orchestration to core systems, identity from Microsoft Entra ID, auditability, and chargeback. The skill stack uses Kong at the edge, FastAPI for policy/audit/cost, and MuleSoft for Process/System APIs.

## Decision
1. **Kong** is the only public/agent ingress. Enforce routing, correlation IDs, rate limits, and (in production) Entra JWT/OIDC validation and mTLS.
2. **FastAPI policy/audit service** records usage, applies demo/local identity gates, and exposes chargeback aggregation. Production must replace demo headers with cryptographically verified token claims and an agent registry.
3. **MuleSoft** owns System/Process APIs for SaaS/legacy connectors, DataWeave canonicalization, and multi-system orchestration. Kong does **not** replace MuleSoft for those concerns.
4. **Avoid double-proxy** when a backend microservice needs no transformation: Kong may route directly after gateway policy. Document each exception in the routing matrix.
5. **Identity split:** preserve end-user delegated identity separately from agent workload identity. Never silently upgrade to app-only permissions for OBO-required resources.

## Consequences
- Clear trust boundaries: Kong edge + MuleSoft independent authz + FastAPI audit.
- Local compose stack demonstrates path only; production requires Entra apps, JWKS validation, secrets vault, TLS, durable audit export.
- Kong OSS demo lacks Enterprise OIDC plugins; plan Konnect/Enterprise or custom JWT plugin validation for production.

## Alternatives considered
- Kong-only (insufficient for SOAP/legacy connectors and canonical models)
- MuleSoft-only edge (weaker K8s-native gateway/traffic features for some topologies)
- Direct agent → backend (fails governance, rate limit, audit, chargeback requirements)
