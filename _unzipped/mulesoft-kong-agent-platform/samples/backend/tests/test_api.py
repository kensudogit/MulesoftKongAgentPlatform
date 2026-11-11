import os
os.environ["DEMO_AUTH"] = "true"
os.environ["DATABASE_URL"] = "sqlite://"
from fastapi.testclient import TestClient
from app.main import app, Base, engine

Base.metadata.create_all(engine)
client = TestClient(app)
HEADERS = {"X-Demo-Agent": "agent-demo", "X-Demo-Department": "it"}

def test_requires_identity():
    assert client.get("/api/v1/usage").status_code == 401

def test_usage_record_and_read():
    response = client.post("/api/v1/usage", headers=HEADERS, json={"api_name": "sample", "request_count": 2, "unit_cost_usd": "0.02"})
    assert response.status_code == 200
    assert response.json()["cost_usd"] == "0.04"
    response = client.get("/api/v1/usage", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["items"][0]["api"] == "sample"

def test_invalid_count():
    assert client.post("/api/v1/usage", headers=HEADERS, json={"api_name": "sample", "request_count": -1}).status_code == 422
