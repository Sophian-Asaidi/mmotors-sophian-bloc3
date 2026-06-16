def test_health_returns_200(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_alerting_simulation(client):
    response = client.post("/health/alert-test")

    assert response.status_code == 200
    assert response.json()["alert_sent"] is True
