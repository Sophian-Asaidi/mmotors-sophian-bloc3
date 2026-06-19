import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_mmotors.db"
os.environ["JWT_SECRET_KEY"] = "test-secret"
os.environ["UPLOAD_DIR"] = "test_uploads"

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app
from app.seed import seed_database


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield
    Base.metadata.drop_all(bind=engine)
    uploads = Path("test_uploads")
    if uploads.exists():
        for item in uploads.rglob("*"):
            if item.is_file():
                item.unlink()


@pytest.fixture
def client():
    return TestClient(app)


def login_headers(client: TestClient, email="client.so@mmotors.fr", password="ClientSo2026!"):
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def admin_headers(client: TestClient):
    return login_headers(client, "admin.so@mmotors.fr", "AdminSo2026!")
