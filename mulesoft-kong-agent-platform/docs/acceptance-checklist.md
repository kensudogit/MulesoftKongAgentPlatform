# Production acceptance checklist

## Local demo progress (this run)
- [x] Skill installed and `validate_skill.py` passed
- [x] Architecture ADR drafted (`docs/ADR-001-platform-placement.md`)
- [x] API routing matrix drafted (`docs/api-routing-matrix.md`)
- [x] Security design documented (`docs/security-design.md`)
- [x] Operations runbook stub (`docs/operations-runbook.md`)
- [x] Cost governance placeholders (`docs/cost-governance.md`)
- [x] OpenAPI draft (`docs/openapi-usage.yaml`)
- [x] Backend unit tests (`pytest` 3 passed)
- [x] Local docker compose stack healthy (`db/api/kong/dashboard` Up)
- [x] Kong / API / Dashboard smoke verified (health 200, usage via Kong, dashboard 200, missing headers 401)
- [x] Entra JWT verifier skeleton + agent registry + quota + structured audit
- [x] Fail-closed tests when `DEMO_AUTH=false` without Entra env (pytest)
- [x] Consumer onboarding, rollout plan, edition matrix, Kong prod example

## Production gate (not claimed complete)
- [ ] Approved API placement matrix and ADR (stakeholder sign-off)
- [ ] Entra tenant, applications, issuer, audiences, scopes and roles defined
- [ ] Cryptographic token validation, OBO vs app-only policy and negative tests implemented
- [ ] Agent registry binding and resource-level authorization implemented
- [ ] No demo headers or default credentials in production
- [ ] TLS/mTLS, private networking, secrets vault and rotation
- [ ] Kong edition/plugin compatibility validated; declarative config reviewed
- [ ] MuleSoft runtime/license and connector compatibility validated
- [ ] OpenAPI, SLO, load, failover, security and integration tests passed
- [ ] Immutable/tamper-evident audit export and retention approved
- [ ] Cost reconciliation, forecasting and budget alerts implemented
- [ ] Runbooks, owners, DR exercises and change approvals complete
