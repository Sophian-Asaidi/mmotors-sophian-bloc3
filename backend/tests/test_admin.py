from tests.conftest import admin_headers, auth_headers


def _create_user_application(client) -> int:
    vehicle = client.get("/vehicles", params={"mode": "rental"}).json()[0]
    response = client.post(
        "/applications",
        data={"vehicle_id": vehicle["id"], "application_type": "rental", "message": "Validation demandée."},
        headers=auth_headers(client),
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_admin_validates_application(client):
    application_id = _create_user_application(client)
    response = client.patch(
        f"/admin/applications/{application_id}/status",
        json={"status": "approved", "admin_comment": "Dossier accepté."},
        headers=admin_headers(client),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "approved"


def test_admin_lists_applications(client):
    response = client.get("/admin/applications", headers=admin_headers(client))

    assert response.status_code == 200
    assert response.json()


def test_user_cannot_create_vehicle(client):
    payload = {
        "brand": "Ford",
        "model": "Puma",
        "year": 2021,
        "mileage": 22000,
        "price": 16900,
        "monthly_price": None,
        "energy": "Essence",
        "transmission": "Manuelle",
        "mode": "sale",
        "status": "available",
    }
    response = client.post("/admin/vehicles", json=payload, headers=auth_headers(client))

    assert response.status_code == 403


def test_admin_switches_vehicle_mode(client):
    vehicle = client.get("/vehicles", params={"mode": "sale"}).json()[0]
    response = client.patch(f"/admin/vehicles/{vehicle['id']}/switch", headers=admin_headers(client))

    assert response.status_code == 200
    assert response.json()["mode"] == "rental"

