"""Production path must deny when DEMO_AUTH is off and Entra is not configured."""
import importlib
import os

import pytest


@pytest.fixture()
def prod_client(monkeypatch):
    monkeypatch.setenv("DEMO_AUTH", "false")
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.delenv("ENTRA_TENANT_ID", raising=False)
    monkeypatch.delenv("ENTRA_AUDIENCE", raising=False)
    monkeypatch.delenv("ENTRA_ISSUER", raising=False)

    import app.auth as auth
    import app.main as main

    importlib.reload(auth)
    importlib.reload(main)
    main.Base.metadata.create_all(main.engine)
    from fastapi.testclient import TestClient

    return TestClient(main.app)


def test_fail_closed_without_token(prod_client):
    response = prod_client.get("/api/v1/usage")
    assert response.status_code == 503
    assert "not configured" in response.json()["detail"].lower() or "deny" in response.json()["detail"].lower()


def test_fail_closed_ignores_demo_headers(prod_client):
    response = prod_client.get(
        "/api/v1/usage",
        headers={"X-Demo-Agent": "agent-demo", "X-Demo-Department": "it"},
    )
    assert response.status_code == 503


def test_bearer_without_entra_config_still_denied(prod_client):
    response = prod_client.get(
        "/api/v1/usage",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 503
