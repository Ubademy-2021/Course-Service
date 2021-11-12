from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_courses():
    response = client.get("/api/courses")
    assert response.status_code == 200


def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200


def test_get_suscriptions():
    response = client.get("/api/suscriptions")
    assert response.status_code == 200
