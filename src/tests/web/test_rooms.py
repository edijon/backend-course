from fastapi.testclient import TestClient
from fastapi import status
from src.tests.persistence import RoomRepositoryDumb, RoomRepositoryException
from src.main.web.main import app
from src.main.web.rooms import Room

API_BASIS = "/api/v1"
API_ROOMS = f"{API_BASIS}/rooms"
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

class TestRoomsEndpoint:
    """Test the rooms endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_given_repository_when_get_rooms_then_get_200_and_rooms_list(self):
        from src.main.web import state
        state.repository_rooms = RoomRepositoryDumb()
        response = self.client.get(API_ROOMS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), Room)

    def test_given_repository_when_get_rooms_raises_exception_then_get_500(self):
        from src.main.web import state
        state.repository_rooms = RoomRepositoryException()
        response = self.client.get(API_ROOMS)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_given_valid_token_when_add_room_then_get_200(self):
        token = get_auth_token()
        room_data = {
            "id": "1",
            "name": "Room 101",
            "description": "First floor room"
        }
        response = self.client.post(API_ROOMS, json=room_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == room_data

    def test_given_invalid_token_when_add_room_then_get_401(self):
        room_data = {
            "id": "1",
            "name": "Room 101",
            "description": "First floor room"
        }
        response = self.client.post(API_ROOMS, json=room_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_update_room_then_get_200(self):
        token = get_auth_token()
        room_data = {
            "id": "1",
            "name": "Room 101",
            "description": "First floor room"
        }
        response = self.client.put(f"{API_ROOMS}/1", json=room_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == room_data

    def test_given_invalid_token_when_update_room_then_get_401(self):
        room_data = {
            "id": "1",
            "name": "Room 101",
            "description": "First floor room"
        }
        response = self.client.put(f"{API_ROOMS}/1", json=room_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_delete_room_then_get_200(self):
        token = get_auth_token()
        response = self.client.delete(f"{API_ROOMS}/1", headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == {"message": "Room deleted"}

    def test_given_invalid_token_when_delete_room_then_get_401(self):
        response = self.client.delete(f"{API_ROOMS}/1", headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
