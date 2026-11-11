"""Structured audit events (no tokens / no PII bodies)."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from .auth import Principal

logger = logging.getLogger("governance.audit")


def emit_audit(
    *,
    action: str,
    principal: Principal,
    api_id: str,
    decision: str,
    request_id: str | None = None,
    extra: dict[str, Any] | None = None,
) -> None:
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "decision": decision,
        "api_id": api_id,
        "agent_id": principal.agent_id,
        "department": principal.department,
        "auth_mode": principal.mode,
        "tid": principal.tid,
        "oid": principal.oid,
        "azp": principal.azp,
        "delegated_user_oid": principal.delegated_user_oid,
        "request_id": request_id,
        "scopes": sorted(principal.scopes),
        "roles": sorted(principal.roles),
    }
    if extra:
        record.update(extra)
    logger.info("audit %s", json.dumps(record, ensure_ascii=False))
