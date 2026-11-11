# Entra ID and agent access control

1. Register distinct applications for API resource, interactive clients, and agent workloads; publish API scopes/app roles.
2. Use Authorization Code + PKCE for user-delegated flows; client credentials with workload identity/certificates for unattended agents where permitted.
3. Validate RS256 JWT with issuer-specific Entra JWKS, issuer, audience, signature, expiry and allowed algorithms; reject unsigned, wrong-audience, expired and unknown-kid tokens.
4. Enforce `scp` for delegated tokens and `roles` for app-only tokens, matching an API-specific authorization matrix. Validate tenant (`tid`) against an allowlist. Treat `oid`+`tid` as principal key; verify `azp`/`appid` client identity as appropriate.
5. Bind agent identity to authenticated client app identity or a protected agent registry; use policy mapping (agent -> allowed API/method/resource, owner, department, quota).
6. Apply ABAC for resource-level decisions, including user permissions for on-behalf-of flows. Never allow agents to bypass human entitlements.
7. Carry `traceparent`, request ID, caller principal, agent registry ID, API ID, policy decision, token issuer and cost attribution into structured audit records. Do not log tokens or request bodies containing PII.
8. Protect against prompt injection/tool misuse using allowlisted tools, explicit argument schemas, approval for sensitive operations, outbound egress restrictions, and request/response data classification.
9. Use mTLS/private networking and secret vault in production. Enforce separate admin/consumer privileges and least privilege.
10. Validate via negative tests: missing token, invalid signature, wrong issuer/audience, insufficient role, cross-tenant, unauthorized agent, over quota, replay/idempotency and injection.

## Deployment note
The provided local sample intentionally does NOT implement a full Entra JWKS verifier. The demo-only identity headers are gated behind `DEMO_AUTH=true`; never expose this mode to a public network. Production rejects all requests until a verified-token integration is implemented and tested.
