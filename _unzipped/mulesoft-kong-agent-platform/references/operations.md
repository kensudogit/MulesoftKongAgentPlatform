# SE standardization and operations

## API lifecycle
Intake -> classify data/API -> choose gateway/integration placement -> threat model -> OpenAPI review -> policy approval -> test -> deploy -> observe -> deprecate.

## Ownership / RACI
Standardization SE: API naming, catalog, OpenAPI linting, nonfunctional acceptance, consumer onboarding, dashboards, release governance.
MuleSoft SE: runtime/environment, connector credentials, transformation, integration SLAs, Anypoint deployment, MuleSoft incident response.
Kong SE: gateway topology, declarative configuration, plugins, certificates, rate limits, Kong incident response.
Security/IAM: Entra apps, role grants, access review, threat model and audit controls.
FinOps: rate cards, allocation, forecasts, budget thresholds.

## Observability
Use W3C Trace Context; OpenTelemetry traces/metrics; redact PII; dashboard traffic, p95/p99 latency, 4xx/5xx, auth denies, policy failures, token validation errors, connector health, cost per API/agent/department.

## Incident and change
Alert on error budget burn, auth spikes, cost anomalies and latency regressions. Runbooks for certificate rollover, JWKS outages, gateway rollback, MuleSoft connector outage, unauthorized tool access and runaway agent loops. Maintain IaC reviews, staging gates, backups and DR drills.

## Adoption
Publish a golden-path starter API, onboarding checklist, architecture decision record, OpenAPI contract, example tokens without real secrets, operational FAQ and office-hour support.
