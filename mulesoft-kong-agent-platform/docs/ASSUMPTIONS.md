# Working assumptions (unconfirmed inputs)

Skill workflow requires gathering real Entra/MuleSoft/Kong values. The following are **working assumptions** used to proceed without fabricated tenant IDs or secrets. Replace before any production design sign-off.

| Item | Assumption | Status |
|------|------------|--------|
| Entra tenant | Single corporate tenant; issuer `https://login.microsoftonline.com/{tenant}/v2.0` | Unconfirmed |
| API inventory | Sample governance API (`/api/v1/usage`) + illustrative Mule Process API (`/api/v1/sample`) | Demo only |
| Backend systems | Placeholder ERP/CRM; no live connectors | Unconfirmed |
| MuleSoft license | Anypoint Platform available; CloudHub 2.0 preferred | Unconfirmed |
| Kong edition | Kong Gateway OSS 3.9 for local demo; Enterprise/Konnect needed for full OIDC plugin features | Partially confirmed (local OSS) |
| SLO | p95 API latency < 500ms (Kong hop < 50ms); availability 99.9%; peak 50 RPS demo | Placeholder |
| Data classification | Usage/cost metadata = Internal; no PII in demo payloads | Assumed |
| Agent identities | `agent-demo`, `dashboard-demo` under department `it` (demo headers only) | Local demo only |
| Goal this run | Local stack + ADR + routing matrix + tests + acceptance tracking | In progress |

**Production fail-closed rule:** `DEMO_AUTH` must remain unset/false outside loopback. Real Entra JWKS validation is mandatory before any public or corporate network exposure.
