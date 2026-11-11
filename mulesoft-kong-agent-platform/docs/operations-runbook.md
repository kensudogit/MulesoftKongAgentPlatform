# Operations runbook (initial)

## Environments
| Env | Purpose | Auth | Notes |
|-----|---------|------|-------|
| local | Skill demo compose | DEMO_AUTH | Loopback only |
| staging | Integration | Entra test tenant | Required before prod |
| production | Live | Entra + mTLS | Fail closed without JWT |

## Ownership (RACI summary)
- Standardization SE: catalog, OpenAPI lint, NFR acceptance, onboarding, release governance
- MuleSoft SE: runtime, connectors, transformations, Anypoint deploy/IR
- Kong SE: gateway topology, decK/declarative config, certs, rate limits, Kong IR
- Security/IAM: Entra apps, role grants, access review, threat model
- FinOps: rate cards, allocation, forecasts, budgets

## Observability targets
- W3C Trace Context + OpenTelemetry
- Dashboards: traffic, p95/p99, 4xx/5xx, auth denies, policy failures, token validation errors, connector health, cost per API/agent/department
- Alerts: error-budget burn, auth spikes, cost anomalies, latency regressions

## Incident runbooks (stubs)
1. **Certificate / JWKS outage** — failover cache TTL; block new sessions if validation impossible; page IAM
2. **Gateway rollback** — redeploy last known-good `kong.yml` / decK state; verify rate-limit and JWT plugins
3. **MuleSoft connector outage** — circuit break Process API; return RFC 9457 problem; open vendor ticket
4. **Unauthorized tool / runaway agent** — revoke agent app role; hard-stop quota; preserve audit export
5. **Demo mode accidentally enabled** — treat as Sev-1; set `DEMO_AUTH=false`; rotate any exposed credentials; review access logs

## Change management
IaC PR review → staging gates → production change window → post-deploy health + auth negative tests → DR drill cadence quarterly (placeholder until approved).
