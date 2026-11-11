"""Per-agent daily quota checks against usage_events."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .registry import AgentPolicy


def assert_within_quota(db: Session, usage_model, policy: AgentPolicy, additional: int = 1) -> None:
    start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    used = db.execute(
        select(func.count(usage_model.id)).where(
            usage_model.agent_id == policy.agent_id,
            usage_model.timestamp >= start,
        )
    ).scalar_one()
    if int(used) + additional > policy.daily_quota:
        raise HTTPException(status_code=429, detail="Agent daily quota exceeded")
