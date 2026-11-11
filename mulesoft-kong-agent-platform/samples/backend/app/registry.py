"""Agent registry and least-privilege policy map (demo data; replace with durable store)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentPolicy:
    agent_id: str
    department: str
    owner: str
    allowed_apis: frozenset[str]
    daily_quota: int
    # Entra app client IDs that may act as this agent (azp/appid). Empty = demo-only binding.
    bound_client_ids: frozenset[str]


# Placeholder registry — no real tenant/client IDs embedded.
AGENT_REGISTRY: dict[str, AgentPolicy] = {
    "agent-demo": AgentPolicy(
        agent_id="agent-demo",
        department="it",
        owner="platform-se",
        allowed_apis=frozenset({"sample", "usage", "gov-usage"}),
        daily_quota=1000,
        bound_client_ids=frozenset(),
    ),
    "dashboard-demo": AgentPolicy(
        agent_id="dashboard-demo",
        department="it",
        owner="platform-se",
        allowed_apis=frozenset({"sample", "usage", "gov-usage"}),
        daily_quota=5000,
        bound_client_ids=frozenset(),
    ),
}


def resolve_agent(agent_id: str) -> AgentPolicy | None:
    return AGENT_REGISTRY.get(agent_id)


def authorize_api(policy: AgentPolicy, api_name: str) -> bool:
    return api_name in policy.allowed_apis
