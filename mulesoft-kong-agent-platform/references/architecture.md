# API management architecture and placement

## Logical flow
Browser/AI Agent -> Entra ID OAuth2 -> Kong API Gateway -> FastAPI policy/audit service -> MuleSoft Process/System APIs -> internal ERP/CRM/core banking systems.
Kong may also route directly to an internal microservice when orchestration or transformation is unnecessary. Avoid blindly double-proxying every request.

## Decision matrix
- Choose **MuleSoft** for SaaS/legacy connectors, SOAP, DataWeave transformation, multi-system orchestration, canonical data models and reusable system/process APIs.
- Choose **Kong** for edge ingress, API gateway, service routing, gateway policy enforcement, rate limiting, traffic management and Kubernetes-native services.
- Choose **both** when the public/agent ingress needs gateway governance and backend calls need MuleSoft transformation/orchestration.
- Prefer neither additional hop if a service mesh/internal trusted architecture already meets requirements; document the decision.

## Nonfunctional design
Define p95/p99 latency and per-hop budgets; availability SLO and error budget; peak RPS and burst; RTO/RPO; encryption at rest/in transit; HA across failure domains; log retention and PII masking; API lifecycle; key rotation; disaster recovery; capacity and spend alerts. Values must be approved, not guessed.

## API contract standards
OpenAPI 3.1, `/api/v1/`, semantic versioning, correlation IDs, idempotency keys for writes, standardized RFC 9457 problem responses, pagination, bounded timeouts, retry with jitter for safe operations, no blind retry on non-idempotent operations.

## Integration contract
Kong -> MuleSoft over private TLS/mTLS where available; forward a short-lived downstream token with correct audience (token exchange or workload token); never simply forward a browser token to an unintended audience. MuleSoft authorizes downstream scopes and logs trace IDs. Avoid duplicated rate-limit policies without documented reason.
