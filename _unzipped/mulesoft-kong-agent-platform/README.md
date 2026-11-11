# MuleSoft × Kong × AI-Agent platform — Claude Code Skill

## Install
Copy the entire `mulesoft-kong-agent-platform` directory into `~/.claude/skills/` (macOS/Linux) or `%USERPROFILE%\.claude\skills\` (Windows). The folder name **must** match the `name` in `SKILL.md`. Restart Claude Code if necessary.

Ask Claude Code: `mulesoft-kong-agent-platform を使い、Entra ID と MuleSoft/Kong を併用する社内AI-Agent API基盤を設計してください。`

## Sample local stack
From this directory run `docker compose up --build -d`. Access API via `http://localhost:8000/docs` or Kong via `http://localhost:8001/api/v1/usage` (demo headers required). Dashboard: `http://localhost:3000`.

Demo request: `curl -H 'X-Demo-Agent: agent-demo' -H 'X-Demo-Department: it' http://localhost:8001/api/v1/usage`

This stack is **local demonstration only**. `DEMO_AUTH=true` uses unverified headers, so never deploy it to a public network. Docker ports bind to loopback. In production remove demo mode, configure Entra OIDC/JWKS validation, TLS, secrets management, mTLS, durable audit pipeline, production database credentials, and a supported Kong/MuleSoft deployment.

## Layout
- `references/`: architecture, security, operations, cost governance
- `samples/backend/`: FastAPI API, PostgreSQL audit/cost model, tests
- `samples/frontend/`: Next.js React TypeScript usage dashboard
- `kong/`: declarative gateway routing (demo only)
- `mulesoft/`: illustrative Mule XML and deployment guide
- `docs/`: API standard, deployment checklist and decision record

## Validation
`python scripts/validate_skill.py` checks frontmatter/folder structure. `cd samples/backend && pip install -r requirements.txt && pytest` runs unit tests. `docker compose config` validates Compose syntax when Docker is installed.
