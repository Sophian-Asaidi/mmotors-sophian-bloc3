from tests.conftest import admin_headers


def test_login_ok(client):
    response = client.post("/auth/login", json={"email": "adminLocal@Motors", "password": "AdminMot1!"})

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"]
    assert data["user"]["role"] == "admin"


def test_register_ok(client):
    response = client.post("/auth/register", json={"email": "new.user@Motors", "password": "MotDePasse1!"})

    assert response.status_code == 201
    assert response.json()["user"]["email"] == "new.user@motors"


def test_email_already_used(client):
    response = client.post("/auth/register", json={"email": "userLocal@Motors", "password": "UserMot1!"})

    assert response.status_code == 409


def test_wrong_password(client):
    response = client.post("/auth/login", json={"email": "adminLocal@Motors", "password": "MauvaisMot1!"})

    assert response.status_code == 401


def test_me_returns_current_user(client):
    response = client.get("/auth/me", headers=admin_headers(client))

    assert response.status_code == 200
    assert response.json()["email"] == "adminlocal@motors"

