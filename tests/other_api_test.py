from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_course_1_students():
    response = client.get("/api/courses/students/1")
    assert response.status_code == 200


def test_get_suscription_from_user():
    response = client.get("/api/suscriptions/inscription/1")
    assert response.status_code == 200


def test_get_suscriptions():
    response = client.get("/api/suscriptions")
    assert response.status_code == 200


def test_get_suscription_1():
    response = client.get("/api/suscriptions/1")
    assert response.status_code == 200


def test_get_suscription_not_exists():
    response = client.get("/api/suscriptions/1231241234523532")
    assert response.status_code == 400


def test_get_collaborators_course_1():
    response = client.get("/api/collaborators/1")
    assert response.status_code == 200


def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200


def test_post_collaborator_bad_user():
    response = client.post("/api/collaborators",
                           json={
                               "courseId": 1,
                               "userId": 121242352351
                           })
    assert response.status_code == 400


def test_post_collaborator_bad_course():
    response = client.post("/api/collaborators",
                           json={
                               "courseId": 121242352351,
                               "userId": 1
                           })
    assert response.status_code == 400


def test_post_course_inscription_bad_course():
    response = client.post("/api/courses/inscription",
                           json={
                               "courseId": 121242352351,
                               "userId": 1
                           })
    assert response.status_code == 400


def test_post_course_inscription_bad_user():
    response = client.post("/api/courses/inscription",
                           json={
                               "courseId": 1,
                               "userId": 121242352351
                           })
    assert response.status_code == 400


def test_post_suscription_inscription_bad_suscription():
    response = client.post("/api/suscriptions/inscription",
                           json={
                               "suscriptionId": 121242352351,
                               "userId": 1
                           })
    assert response.status_code == 400


def test_post_suscription_inscription_bad_user():
    response = client.post("/api/suscriptions/inscription",
                           json={
                               "suscriptionId": 1,
                               "userId": 121242352351
                           })
    assert response.status_code == 400


def test_post_suscription_course_bad_suscription():
    response = client.post("/api/suscriptions/course",
                           json={
                               "suscriptionId": 121242352351,
                               "courseId": 1
                           })
    assert response.status_code == 400


def test_post_suscription_course_bad_course():
    response = client.post("/api/suscriptions/course",
                           json={
                               "suscriptionId": 1,
                               "courseId": 121242352351
                           })
    assert response.status_code == 400
