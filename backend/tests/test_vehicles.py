from tests.conftest import admin_headers


def test_list_vehicles(client):
    response = client.get("/vehicles")

    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_filter_sale_vehicles(client):
    response = client.get("/vehicles", params={"mode": "sale"})

    assert response.status_code == 200
    assert response.json()
    assert {vehicle["mode"] for vehicle in response.json()} == {"sale"}


def test_filter_rental_vehicles(client):
    response = client.get("/vehicles", params={"mode": "location"})

    assert response.status_code == 200
    assert response.json()
    assert {vehicle["mode"] for vehicle in response.json()} == {"rental"}


def test_admin_create_vehicle(client):
    payload = {
        "brand": "Toyota",
        "model": "Yaris",
        "year": 2022,
        "mileage": 18000,
        "price": 15990,
        "monthly_price": None,
        "energy": "Hybride",
        "transmission": "Automatique",
        "mode": "sale",
        "status": "available",
    }
    response = client.post("/admin/vehicles", json=payload, headers=admin_headers(client))

    assert response.status_code == 201
    assert response.json()["brand"] == "Toyota"

