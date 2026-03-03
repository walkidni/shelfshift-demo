from fastapi.testclient import TestClient


def test_create_app_health_endpoint() -> None:
    from shelfshift_demo.main import create_app

    client = TestClient(create_app())
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
