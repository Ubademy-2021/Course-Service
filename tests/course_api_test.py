from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_courses():
    response = client.get("/api/courses")
    assert response.status_code == 200


def test_get_course_id_1():
    response = client.get("/api/courses?course_id=1")
    assert response.status_code == 200


def test_get_course_id_not_exists():
    response = client.get("/api/courses?course_id=2342342342342")
    assert response.status_code == 400


def test_get_courses_active_true():
    response = client.get("/api/courses?active=True")
    assert response.status_code == 200


def test_get_courses_with_category_1():
    response = client.get("/api/courses?category_id=1")
    assert response.status_code == 200


def test_get_courses_with_suscription_1():
    response = client.get("/api/courses?suscription_id=1")
    assert response.status_code == 200


def test_get_courses_with_student_id_1():
    response = client.get("/api/courses?user_id=1")
    assert response.status_code == 200


def test_get_courses_active():
    response = client.get("/api/courses/active")
    assert response.status_code == 200


def test_get_course_recommendation_id_1():
    response = client.get("/api/courses/recommendation/1")
    assert response.status_code == 200


def test_post_course_category_bad_course():
    response = client.post("/api/courses/category",
                           json={
                               "courseId": 121242352351,
                               "categoryId": 1
                           })
    assert response.status_code == 400


def test_post_course_category_bad_category():
    response = client.post("/api/courses/category",
                           json={
                               "courseId": 1,
                               "categoryId": 121242352351
                           })
    assert response.status_code == 400
