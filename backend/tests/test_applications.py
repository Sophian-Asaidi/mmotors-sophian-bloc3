from tests.conftest import auth_headers


def _first_vehicle_id(client, mode: str) -> int:
    response = client.get("/vehicles", params={"mode": mode})
    assert response.status_code == 200
    return response.json()[0]["id"]


def test_submit_application_with_document(client):
    vehicle_id = _first_vehicle_id(client, "rental")
    response = client.post(
        "/applications",
        data={"vehicle_id": vehicle_id, "application_type": "rental", "message": "Dossier complet."},
        files={"documents": ("piece-identite.pdf", b"demo pdf", "application/pdf")},
        headers=auth_headers(client),
    )

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["documents"][0]["filename"] == "piece-identite.pdf"


def test_follow_my_applications(client):
    response = client.get("/applications/me", headers=auth_headers(client))

    assert response.status_code == 200
    assert response.json()


def test_application_access_refused_without_token(client):
    response = client.get("/applications/me")

    assert response.status_code == 401


def test_rejects_wrong_application_type_for_vehicle(client):
    vehicle_id = _first_vehicle_id(client, "sale")
    response = client.post(
        "/applications",
        data={"vehicle_id": vehicle_id, "application_type": "rental"},
        headers=auth_headers(client),
    )

    assert response.status_code == 400

