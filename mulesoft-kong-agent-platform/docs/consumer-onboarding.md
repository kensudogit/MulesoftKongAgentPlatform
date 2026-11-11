# Consumer / AI-Agent onboarding checklist

1. Submit API intake: purpose, data classification, expected RPS, owner department, agent ID.
2. Standardization SE reviews OpenAPI and placement matrix (Kong-only / MuleSoft / both).
3. Security/IAM registers Entra apps (resource + agent client); grants scopes/roles; binds agent to registry.
4. Kong SE adds route/plugins (JWT/OIDC edition-dependent, rate limit, correlation ID); no demo headers.
5. MuleSoft SE (if required) publishes System/Process API to Exchange and applies API Manager policies.
6. FinOps assigns rate card, department budget, and per-agent daily quota.
7. Staging: contract tests, negative auth tests, load smoke, audit sample verification.
8. Production change approval; publish runbook contacts; schedule access review.
