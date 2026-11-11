"""Entra-mode regressions: agent/client binding, quota by request_count, JWKS client reuse.

Tokens are signed with a throwaway RSA key generated in-test; JWKS fetch is stubbed.
"""
import importlib
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

TENANT = "00000000-0000-0000-0000-000000000000"
AUDIENCE = "api://agent-governance-test"
BOUND_CLIENT = "client-bound"


@pytest.fixture(scope="module")
def signing_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture()
def env(monkeypatch, signing_key):
    monkeypatch.setenv("DEMO_AUTH", "false")
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.setenv("ENTRA_TENANT_ID", TENANT)
    monkeypatch.setenv("ENTRA_AUDIENCE", AUDIENCE)
    monkeypatch.delenv("ENTRA_ISSUER", raising=False)
    monkeypatch.delenv("ENTRA_REQUIRED_ROLES", raising=False)
    monkeypatch.delenv("ENTRA_REQUIRED_SCOPES", raising=False)

    import app.auth as auth
    import app.main as main
    import app.registry as registry

    importlib.reload(auth)
    importlib.reload(main)
    main.Base.metadata.create_all(main.engine)

    constructed = {"n": 0}

    class _Key:
        key = signing_key.public_key()

    class _FakeJWKS:
        def __init__(self, *args, **kwargs):
            constructed["n"] += 1

        def get_signing_key_from_jwt(self, _token):
            return _Key()

    monkeypatch.setattr(auth, "PyJWKClient", _FakeJWKS)
    monkeypatch.setitem(
        registry.AGENT_REGISTRY,
        "agent-bound",
        registry.AgentPolicy(
            agent_id="agent-bound",
            department="it",
            owner="test",
            allowed_apis=frozenset({"sample"}),
            daily_quota=10,
            bound_client_ids=frozenset({BOUND_CLIENT}),
        ),
    )
    return TestClient(main.app), constructed


def _headers(key, agent="agent-bound", **claims):
    payload = {
        "iss": f"https://login.microsoftonline.com/{TENANT}/v2.0",
        "aud": AUDIENCE,
        "exp": int(time.time()) + 600,
        "tid": TENANT,
        "oid": "oid-test",
        "azp": BOUND_CLIENT,
        "scp": "access_as_agent",
    }
    payload.update(claims)
    return {
        "Authorization": "Bearer " + jwt.encode(payload, key, algorithm="RS256"),
        "X-Agent-Id": agent,
    }


def test_bound_client_allowed(env, signing_key):
    client, _ = env
    assert client.get("/api/v1/usage", headers=_headers(signing_key)).status_code == 200


def test_unbound_client_cannot_claim_agent(env, signing_key):
    client, _ = env
    r = client.get("/api/v1/usage", headers=_headers(signing_key, azp="client-other"))
    assert r.status_code == 403


def test_agent_without_binding_denied_in_entra_mode(env, signing_key):
    # agent-demo has no bound_client_ids: it must not be reachable with any Entra token.
    client, _ = env
    r = client.get("/api/v1/usage", headers=_headers(signing_key, agent="agent-demo"))
    assert r.status_code == 403


def test_quota_counts_requests_not_rows(env, signing_key):
    client, _ = env
    h = _headers(signing_key)
    body = {"api_name": "sample", "request_count": 9}
    assert client.post("/api/v1/usage", headers=h, json=body).status_code == 200
    # 9 used of 10: another batch of 9 must be rejected (previously counted as 1 row).
    assert client.post("/api/v1/usage", headers=h, json=body).status_code == 429
    ok = {"api_name": "sample", "request_count": 1}
    assert client.post("/api/v1/usage", headers=h, json=ok).status_code == 200
    assert client.post("/api/v1/usage", headers=h, json=ok).status_code == 429


def test_jwks_client_reused_across_requests(env, signing_key):
    client, constructed = env
    for _ in range(3):
        client.get("/api/v1/usage", headers=_headers(signing_key))
    assert constructed["n"] == 1
