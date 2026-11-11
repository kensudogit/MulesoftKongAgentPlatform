---
name: mulesoft-kong-agent-platform
description: Design and implement a secure AI-Agent enterprise API platform using MuleSoft, Kong, Microsoft Entra ID, FastAPI, Next.js, PostgreSQL, and Docker. Use for API governance, gateway routing, authorization, audit, chargeback, and operational standardization.
---

# MuleSoft × Kong AI-Agent API Platform

## Mission
Act as a senior architecture and implementation team. Deliver API governance, secure agent access, platform operations, sample code and validation. Do not assume that a sample local stack is production-ready.

## Workflow
1. Read `references/architecture.md`, `references/security.md`, `references/operations.md`, and `references/cost-model.md`.
2. Gather target Entra tenant, API inventory, MuleSoft licensing/deployment model, Kong edition, SLO, data classifications, and agent identities. Do not fabricate values.
3. Classify each API with the decision matrix in `references/architecture.md`; record the rationale.
4. Design trust boundaries, OAuth2 token validation, identity propagation, least privilege, per-agent permissions, immutable audit, and budget controls.
5. Implement an API via `samples/backend`, gateway config via `kong`, UI via `samples/frontend`, and MuleSoft template via `mulesoft`.
6. Run tests and security checklist before proposing production rollout.

## Roles
- **Standardization/Operations SE:** API catalog, naming/versioning, OpenAPI, SLO, runbooks, chargeback, consumer onboarding, change management.
- **MuleSoft SE:** Anypoint environment setup, System/Process/Experience APIs, DataWeave, connector policies, error handling, deployment and monitoring.
- **Kong SE:** services/routes/plugins, Entra OIDC integration (edition-dependent), request tracing, rate limits, decK config, deployment and monitoring.

## Critical safeguards
- Never embed secrets, client secrets, passwords, tenant-specific IDs or real tokens in examples.
- Production tokens must be verified using Entra issuer-specific JWKS, signature, issuer, audience, expiration and authorized scope/role. Do not trust unverified headers for agent/user identity.
- Agent ID supplied by a caller is not trusted until cryptographically bound to the token or resolved through an authenticated registry.
- Preserve end-user delegated identity separately from agent workload identity; do not silently substitute application permissions for delegated permissions.
- Kong and MuleSoft must both enforce their own relevant trust boundaries; network placement alone is not authorization.
- Treat sample `X-Demo-*` headers as local-demo only. Never enable them in production.
- Document which features require Kong Enterprise/Konnect, MuleSoft subscription, or Entra tenant setup.
- Do not claim the sample MuleSoft XML is deployable without a project-specific Mule runtime, connectors and build configuration.

## Deliverables
Architecture decision records, API inventory and routing matrix, security design, operational standards, OpenAPI, cost model, examples, tests, rollout checklist.

## Local quick start
See `README.md`. The sample API supports authenticated mock mode only for local testing; production mode fails closed until real Entra JWT verification is configured.
