# Production acceptance checklist

- [ ] Approved API placement matrix and ADR
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
