import os

os.environ["DEMO_AUTH"] = "true"
os.environ["DATABASE_URL"] = "sqlite://"
os.environ.pop("ENTRA_TENANT_ID", None)
os.environ.pop("ENTRA_AUDIENCE", None)

from fastapi.testclient import TestClient
from app.main import Base, app, engine

Base.metadata.create_all(engine)
client = TestClient(app)
HEADERS = {"X-Demo-Agent": "agent-demo", "X-Demo-Department": "it"}


def test_requires_identity():
    assert client.get("/api/v1/usage").status_code == 401


def test_usage_record_and_read():
    response = client.post(
        "/api/v1/usage",
        headers=HEADERS,
        json={"api_name": "sample", "request_count": 2, "unit_cost_usd": "0.02"},
    )
    assert response.status_code == 200
    assert response.json()["cost_usd"] == "0.04"
    response = client.get("/api/v1/usage", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["items"][0]["api"] == "sample"


def test_invalid_count():
    assert (
        client.post(
            "/api/v1/usage", headers=HEADERS, json={"api_name": "sample", "request_count": -1}
        ).status_code
        == 422
    )


def test_unknown_demo_agent_denied():
    bad = {"X-Demo-Agent": "unknown-agent", "X-Demo-Department": "it"}
    assert client.get("/api/v1/usage", headers=bad).status_code == 403


def test_department_mismatch_denied():
    bad = {"X-Demo-Agent": "agent-demo", "X-Demo-Department": "finance"}
    assert client.get("/api/v1/usage", headers=bad).status_code == 403


def test_health_reports_demo_mode():
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["demo_auth"] is True
