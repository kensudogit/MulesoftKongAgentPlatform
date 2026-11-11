# Rollout plan (staging → production)

## Phase 0 — Local (done in this skill run)
- Compose demo with `DEMO_AUTH=true` on loopback
- Unit tests including fail-closed when demo is off
- ADR, routing matrix, security/ops/cost docs

## Phase 1 — Staging (blocked on real inputs)
Provide without pasting secrets into git:
- `ENTRA_TENANT_ID`, `ENTRA_AUDIENCE`, optional `ENTRA_ISSUER` / `ENTRA_JWKS_URL`
- `ENTRA_ALLOWED_TIDS`, `ENTRA_REQUIRED_SCOPES` / `ENTRA_REQUIRED_ROLES`
- Agent registry entries with real `bound_client_ids`
- Kong edition decision (OSS JWT plugin vs Enterprise OIDC / Konnect)
- MuleSoft runtime target (CloudHub 2.0 / RTF / on-prem)

## Phase 2 — Hardening
- Disable `DEMO_AUTH` everywhere non-loopback
- TLS/mTLS, private networking, secrets vault
- Immutable audit export and retention policy
- Budget hard-stops with critical-API exceptions approved
- Negative test suite in CI (signature, audience, tenant, quota, unknown agent)

## Phase 3 — Production
- Change window + rollback of Kong declarative config
- Dual authorization: Kong edge + MuleSoft API Manager
- Access review and DR drill scheduled

## Environment variables (API service)
| Variable | Purpose |
|----------|---------|
| `DEMO_AUTH` | `true` only on loopback demo |
| `ENTRA_TENANT_ID` | Tenant for issuer/JWKS defaults |
| `ENTRA_AUDIENCE` | API app audience |
| `ENTRA_ISSUER` | Override issuer URL |
| `ENTRA_JWKS_URL` | Override JWKS |
| `ENTRA_ALLOWED_TIDS` | Comma allowlist |
| `ENTRA_REQUIRED_SCOPES` | Space-separated delegated scopes |
| `ENTRA_REQUIRED_ROLES` | Comma-separated app roles |
| `DATABASE_URL` | Postgres connection |
