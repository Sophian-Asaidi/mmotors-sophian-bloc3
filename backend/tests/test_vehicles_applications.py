from tests.conftest import admin_headers, login_headers


def test_catalog_filter(client):
    sale = client.get("/vehicles?mode=sale")
    rent = client.get("/vehicles?mode=rent")
    assert sale.status_code == 200
    assert rent.status_code == 200
    assert all(vehicle["mode"] == "sale" for vehicle in sale.json())
    assert all(vehicle["mode"] == "rent" for vehicle in rent.json())


def test_client_submit_application(client):
    vehicle = client.get("/vehicles?mode=sale").json()[0]
    response = client.post(
        "/applications",
        data={"vehicle_id": vehicle["id"], "offer_type": "sale", "message": "Je suis intéressé."},
        files=[("documents", ("piece.pdf", b"fake pdf", "application/pdf"))],
        headers=login_headers(client),
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["documents"][0]["filename"] == "piece.pdf"


def test_forbidden_file_upload(client):
    vehicle = client.get("/vehicles?mode=sale").json()[0]
    response = client.post(
        "/applications",
        data={"vehicle_id": vehicle["id"], "offer_type": "sale", "message": "Test fichier."},
        files=[("documents", ("script.exe", b"danger", "application/x-msdownload"))],
        headers=login_headers(client),
    )
    assert response.status_code == 400


def test_admin_creates_vehicle_and_changes_mode(client):
    headers = admin_headers(client)
    created = client.post(
        "/admin/vehicles",
        json={
            "brand": "Citroen",
            "model": "C4",
            "year": 2022,
            "mileage": 14000,
            "energy": "Essence",
            "transmission": "Manuelle",
            "mode": "sale",
            "price": 18900,
        },
        headers=headers,
    )
    assert created.status_code == 201
    vehicle_id = created.json()["id"]
    changed = client.patch(f"/admin/vehicles/{vehicle_id}/mode", json={"mode": "rent", "monthly_price": 299}, headers=headers)
    assert changed.status_code == 200
    assert changed.json()["mode"] == "rent"


def test_admin_decides_application(client):
    application_id = client.get("/admin/applications", headers=admin_headers(client)).json()[0]["id"]
    response = client.patch(
        f"/admin/applications/{application_id}/status",
        json={"status": "approved", "admin_comment": "Dossier complet"},
        headers=admin_headers(client),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
