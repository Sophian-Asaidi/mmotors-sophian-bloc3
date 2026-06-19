def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "ok"


def test_metrics(client):
    client.get("/health")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "mmotors_requests_total" in response.text


def test_alert(client):
    response = client.post("/health/alert-test?reason=test")
    assert response.status_code == 200
    assert response.json()["status"] == "alert_simulated"
