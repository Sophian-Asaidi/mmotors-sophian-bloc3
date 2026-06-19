from tests.conftest import admin_headers


def test_login_admin(client):
    response = client.post("/auth/login", json={"email": "admin.so@mmotors.fr", "password": "AdminSo2026!"})
    assert response.status_code == 200
    assert response.json()["user"]["role"] == "admin"
    assert response.json()["access_token"]


def test_register_and_me(client):
    response = client.post("/auth/register", json={"email": "nouveau@mmotors.fr", "password": "Password2026!"})
    assert response.status_code == 201
    token = response.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "nouveau@mmotors.fr"


def test_duplicate_email(client):
    response = client.post("/auth/register", json={"email": "client.so@mmotors.fr", "password": "ClientSo2026!"})
    assert response.status_code == 409


def test_admin_route_requires_admin(client):
    response = client.get("/admin/applications", headers=admin_headers(client))
    assert response.status_code == 200
