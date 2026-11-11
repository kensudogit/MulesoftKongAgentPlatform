# Security design (demo vs production)

## Local demo (current)
- `DEMO_AUTH=true` accepts `X-Demo-Agent` / `X-Demo-Department` **without cryptographic verification**.
- Ports bound to `127.0.0.1` only.
- Postgres password is a local placeholder (`local_only_password`).
- Kong declarative config: correlation-id + rate-limiting (120/min). No JWT plugin in OSS demo.

## Production requirements (must implement before exposure)
1. Register distinct Entra apps: API resource, interactive clients, agent workloads; publish scopes/app roles.
2. User flows: Authorization Code + PKCE. Unattended agents: client credentials / workload identity with certificates where permitted.
3. Validate RS256 JWT via issuer-specific JWKS: issuer, audience, signature, expiry, allowed algorithms; reject unsigned/wrong-audience/expired/unknown-kid.
4. Enforce `scp` (delegated) and `roles` (app-only); allowlist `tid`; principal key `oid`+`tid`; verify `azp`/`appid`.
5. Bind agent ID to authenticated client app or protected agent registry; map agent → allowed API/method/resource, owner, department, quota.
6. ABAC for resource-level decisions; agents must not bypass human entitlements on OBO paths.
7. Structured audit: traceparent, request ID, principal, agent registry ID, API ID, policy decision, token issuer, cost attribution. Never log tokens or PII bodies.
8. Prompt-injection / tool-misuse controls: allowlisted tools, argument schemas, approval for sensitive ops, egress restrictions.
9. mTLS/private networking + secrets vault; separate admin/consumer privileges.
10. Negative tests: missing token, bad signature, wrong issuer/audience, insufficient role, cross-tenant, unauthorized agent, over quota, replay/idempotency, injection.

## Explicit non-claims
- Sample does **not** implement Entra JWKS verification.
- Sample Mule XML is **not** a deployable project.
- Demo headers must **never** be enabled on non-loopback networks.
