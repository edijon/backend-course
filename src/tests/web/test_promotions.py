from fastapi.testclient import TestClient
from fastapi import status
from src.tests.persistence import PromotionRepositoryDumb, PromotionRepositoryException
from src.main.web.main import app
from src.main.web.promotions import Promotion

API_BASIS = "/api/v1"
API_PROMOTIONS = f"{API_BASIS}/promotions"
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

class TestPromotionsEndpoint:
    """Test the promotions endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_given_repository_when_get_promotions_then_get_200_and_promotions_list(self):
        from src.main.web import state
        state.repository_promotions = PromotionRepositoryDumb()
        response = self.client.get(API_PROMOTIONS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), Promotion)

    def test_given_repository_when_get_promotions_raises_exception_then_get_500(self):
        from src.main.web import state
        state.repository_promotions = PromotionRepositoryException()
        response = self.client.get(API_PROMOTIONS)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_given_valid_token_when_add_promotion_then_get_200(self):
        token = get_auth_token()
        promotion_data = {
            "id": "1",
            "study_year": 2,
            "diploma": "DEUST",
            "name": "Kempf"
        }
        response = self.client.post(API_PROMOTIONS, json=promotion_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == promotion_data

    def test_given_invalid_token_when_add_promotion_then_get_401(self):
        promotion_data = {
            "id": "1",
            "study_year": 2,
            "diploma": "DEUST",
            "name": "Kempf"
        }
        response = self.client.post(API_PROMOTIONS, json=promotion_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_update_promotion_then_get_200(self):
        token = get_auth_token()
        promotion_data = {
            "id": "1",
            "study_year": 2,
            "diploma": "DEUST",
            "name": "Kempf"
        }
        response = self.client.put(f"{API_PROMOTIONS}/1", json=promotion_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == promotion_data

    def test_given_invalid_token_when_update_promotion_then_get_401(self):
        promotion_data = {
            "id": "1",
            "study_year": 2,
            "diploma": "DEUST",
            "name": "Kempf"
        }
        response = self.client.put(f"{API_PROMOTIONS}/1", json=promotion_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_delete_promotion_then_get_200(self):
        token = get_auth_token()
        response = self.client.delete(f"{API_PROMOTIONS}/1", headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == {"message": "Promotion deleted"}

    def test_given_invalid_token_when_delete_promotion_then_get_401(self):
        response = self.client.delete(f"{API_PROMOTIONS}/1", headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)
