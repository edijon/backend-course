from fastapi.testclient import TestClient
from fastapi import status
from src.tests.persistence import TeacherRepositoryDumb, TeacherRepositoryException
from src.main.web.main import app
from src.main.web.teachers import Teacher

API_BASIS = "/api/v1"
API_TEACHERS = f"{API_BASIS}/teachers"
API_TOKEN = "/token"

client = TestClient(app)

def get_auth_token():
    response = client.post(API_TOKEN, data={"username": "user", "password": "password"})
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json()["access_token"]

def assert_response_status(response, expected_status):
    assert response.status_code == expected_status, response.text

def assert_list_of_models(json_list, model_class, min_length=2):
    assert isinstance(json_list, list)
    assert len(json_list) >= min_length
    for item in json_list:
        model_class(**item)

class TestTeachersEndpoint:
    """Test the teachers endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_given_repository_when_get_teachers_then_get_200_and_teachers_list(self):
        from src.main.web import state
        state.repository_teachers = TeacherRepositoryDumb()
        response = self.client.get(API_TEACHERS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), Teacher)

    def test_given_repository_when_get_teachers_raises_exception_then_get_500(self):
        from src.main.web import state
        state.repository_teachers = TeacherRepositoryException()
        response = self.client.get(API_TEACHERS)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_given_valid_token_when_add_teacher_then_get_200(self):
        token = get_auth_token()
        teacher_data = {
            "id": "1",
            "name": "Doe",
            "firstname": "John"
        }
        response = self.client.post(API_TEACHERS, json=teacher_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == teacher_data

    def test_given_invalid_token_when_add_teacher_then_get_401(self):
        teacher_data = {
            "id": "1",
            "name": "Doe",
            "firstname": "John"
        }
        response = self.client.post(API_TEACHERS, json=teacher_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_update_teacher_then_get_200(self):
        token = get_auth_token()
        teacher_data = {
            "id": "1",
            "name": "Doe",
            "firstname": "John"
        }
        response = self.client.put(f"{API_TEACHERS}/1", json=teacher_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == teacher_data

    def test_given_invalid_token_when_update_teacher_then_get_401(self):
        teacher_data = {
            "id": "1",
            "name": "Doe",
            "firstname": "John"
        }
        response = self.client.put(f"{API_TEACHERS}/1", json=teacher_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_delete_teacher_then_get_200(self):
        token = get_auth_token()
        response = self.client.delete(f"{API_TEACHERS}/1", headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == {"message": "Teacher deleted"}

    def test_given_invalid_token_when_delete_teacher_then_get_401(self):
        response = self.client.delete(f"{API_TEACHERS}/1", headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
