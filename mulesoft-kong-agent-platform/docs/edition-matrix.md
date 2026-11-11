# Feature × product edition matrix

| Capability | Kong Gateway OSS | Kong Enterprise / Konnect | MuleSoft Anypoint | Entra ID tenant |
|------------|------------------|---------------------------|-------------------|-----------------|
| Declarative routing / rate limit | Yes (local demo) | Yes | N/A | N/A |
| Correlation ID | Yes | Yes | Via policies/logs | N/A |
| OIDC / advanced IdP plugins | Limited / DIY | Yes (typical path) | API Manager OAuth2/JWT | App registrations |
| Entra JWKS validation in sample API | FastAPI `auth.py` | Same + gateway option | Independent JWT policy | Issuer/JWKS |
| System/Process API + connectors | N/A | N/A | Required | N/A |
| Chargeback UI sample | Next.js demo | Same | N/A | N/A |

Do not claim Enterprise-only plugins work on OSS without verification.
