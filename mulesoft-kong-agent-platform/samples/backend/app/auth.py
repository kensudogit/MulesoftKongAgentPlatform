"""Identity resolution: local demo headers OR Entra JWT (fail closed)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Annotated, Any

import jwt
from fastapi import Header, HTTPException, status
from jwt import PyJWKClient

from .registry import resolve_agent


@dataclass(frozen=True)
class Principal:
    agent_id: str
    department: str
    mode: str  # "demo" | "entra"
    tid: str | None = None
    oid: str | None = None
    azp: str | None = None
    scopes: frozenset[str] = frozenset()
    roles: frozenset[str] = frozenset()
    delegated_user_oid: str | None = None


def _env_true(name: str) -> bool:
    return os.getenv(name, "false").lower() in {"1", "true", "yes"}


def demo_auth_enabled() -> bool:
    return _env_true("DEMO_AUTH")


def entra_configured() -> bool:
    return bool(
        os.getenv("ENTRA_TENANT_ID")
        and os.getenv("ENTRA_AUDIENCE")
        and (os.getenv("ENTRA_ISSUER") or os.getenv("ENTRA_TENANT_ID"))
    )


def _issuer() -> str:
    explicit = os.getenv("ENTRA_ISSUER", "").strip()
    if explicit:
        return explicit.rstrip("/")
    tenant = os.getenv("ENTRA_TENANT_ID", "").strip()
    return f"https://login.microsoftonline.com/{tenant}/v2.0"


def _jwks_url() -> str:
    explicit = os.getenv("ENTRA_JWKS_URL", "").strip()
    if explicit:
        return explicit
    tenant = os.getenv("ENTRA_TENANT_ID", "").strip()
    return f"https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys"


def _allowed_tids() -> set[str]:
    raw = os.getenv("ENTRA_ALLOWED_TIDS", os.getenv("ENTRA_TENANT_ID", ""))
    return {x.strip() for x in raw.split(",") if x.strip()}


def _required_scopes() -> set[str]:
    raw = os.getenv("ENTRA_REQUIRED_SCOPES", "access_as_agent")
    return {x.strip() for x in raw.split() if x.strip()}  # space-separated like JWT scp


def _required_roles() -> set[str]:
    raw = os.getenv("ENTRA_REQUIRED_ROLES", "")
    return {x.strip() for x in raw.split(",") if x.strip()}


def verify_entra_bearer(authorization: str | None) -> dict[str, Any]:
    # Fail closed until Entra verification env is present — do not accept demo headers here.
    if not entra_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Production identity verification not configured; deny by default",
        )
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ", 1)[1].strip()
    audience = os.getenv("ENTRA_AUDIENCE", "")
    issuer = _issuer()
    jwks_client = PyJWKClient(_jwks_url(), cache_keys=True)
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=audience,
            issuer=issuer,
            options={
                "require": ["exp", "iss", "aud"],
                "verify_signature": True,
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
            },
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc.__class__.__name__}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    tid = str(claims.get("tid") or "")
    allowed = _allowed_tids()
    if allowed and tid not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tenant not allowed")

    scp = frozenset(str(claims.get("scp") or "").split())
    roles = claims.get("roles") or []
    role_set = frozenset(roles if isinstance(roles, list) else [str(roles)])

    need_scopes = _required_scopes()
    need_roles = _required_roles()
    # Delegated tokens use scp; app-only use roles. Accept either matching path.
    scope_ok = bool(need_scopes & scp) if need_scopes else True
    role_ok = bool(need_roles & role_set) if need_roles else (not need_scopes or scope_ok)
    if need_scopes and need_roles:
        if not (scope_ok or role_ok):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope/role")
    elif need_scopes and not scope_ok:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient scope")
    elif need_roles and not role_ok:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")

    return claims


def principal_from_claims(claims: dict[str, Any], agent_hint: str | None) -> Principal:
    azp = str(claims.get("azp") or claims.get("appid") or "")
    tid = str(claims.get("tid") or "")
    oid = str(claims.get("oid") or "")
    scp = frozenset(str(claims.get("scp") or "").split())
    roles = claims.get("roles") or []
    role_set = frozenset(roles if isinstance(roles, list) else [str(roles)])

    # Prefer claim-bound agent id; never trust free-form hint unless registry binds azp.
    agent_id = str(claims.get("agent_id") or claims.get("extension_AgentId") or agent_hint or "")
    if not agent_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Agent identity not bound to token")

    policy = resolve_agent(agent_id)
    if policy is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unknown agent")

    if policy.bound_client_ids and azp not in policy.bound_client_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Agent/client binding mismatch")

    # OBO: preserve end-user oid separately when present (idtyp != app).
    delegated = oid if claims.get("idtyp") != "app" else None

    return Principal(
        agent_id=policy.agent_id,
        department=policy.department,
        mode="entra",
        tid=tid or None,
        oid=oid or None,
        azp=azp or None,
        scopes=scp,
        roles=role_set,
        delegated_user_oid=delegated,
    )


async def require_principal(
    authorization: Annotated[str | None, Header()] = None,
    x_demo_agent: Annotated[str | None, Header()] = None,
    x_demo_department: Annotated[str | None, Header()] = None,
    x_agent_id: Annotated[str | None, Header()] = None,
) -> Principal:
    """Resolve caller identity. Demo headers only when DEMO_AUTH=true."""
    if demo_auth_enabled():
        if not x_demo_agent or not x_demo_department:
            raise HTTPException(status_code=401, detail="Local demo identity headers required")
        if len(x_demo_agent) > 120 or len(x_demo_department) > 120:
            raise HTTPException(status_code=400, detail="Invalid demo identity")
        policy = resolve_agent(x_demo_agent)
        if policy is None:
            raise HTTPException(status_code=403, detail="Unknown demo agent")
        if policy.department != x_demo_department:
            raise HTTPException(status_code=403, detail="Department mismatch for agent")
        return Principal(agent_id=policy.agent_id, department=policy.department, mode="demo")

    claims = verify_entra_bearer(authorization)
    return principal_from_claims(claims, x_agent_id)
