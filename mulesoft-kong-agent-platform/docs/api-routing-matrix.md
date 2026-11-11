# API inventory and routing matrix

## Inventory (demo + planned)

| API ID | Path | Owner | Data class | Auth (prod) | Placement | Rationale |
|--------|------|-------|------------|-------------|-----------|-----------|
| GOV-USAGE | `/api/v1/usage` | Platform SE | Internal (cost metadata) | Entra JWT + agent registry | **Kong → FastAPI** | Pure governance/audit/chargeback; no Mule transformation needed |
| MULE-SAMPLE | `/api/v1/sample` | MuleSoft SE | Internal | Entra JWT + Mule API Manager policy | **Kong → MuleSoft Process API → System API** | Illustrative orchestration/canonical response; requires real Mule project |
| (future) ERP-READ | TBD | Domain SE | Confidential | Delegated OBO + scopes | **Kong → MuleSoft System API** | Legacy/SaaS connector + field mapping → choose MuleSoft |
| (future) K8S-MSVC | TBD | App SE | Internal | App roles / mTLS | **Kong → microservice** | No orchestration → skip Mule hop |

## Decision matrix application
- **MuleSoft:** connectors, SOAP, DataWeave, multi-system orchestration, canonical models.
- **Kong:** ingress, routing, gateway policy, rate limit, traffic management.
- **Both:** agent/public ingress needs gateway governance **and** backend needs Mule transformation.
- **Neither extra hop:** only when mesh/internal trust already satisfies requirements and is documented.

## Local demo path
```
Browser/curl
  -> Kong :8001 (/api/v1*)
    -> FastAPI :8000
      -> PostgreSQL (usage_events)
Dashboard :3000 -> FastAPI :8000 (server-side fetch, demo headers)
```

MuleSoft sample XML is **not** wired into docker-compose; treat as Anypoint project fragment only.
