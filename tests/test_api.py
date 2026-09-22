from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_parse_endpoint() -> None:
    response = client.post(
        "/parse",
        json={"text": "Client email: sam@example.com\n- Submit application by 2026-10-01."},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["contact"]["emails"] == ["sam@example.com"]
    assert payload["action_items"][0]["due_date"] == "2026-10-01"
