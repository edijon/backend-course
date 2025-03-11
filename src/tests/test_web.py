from fastapi.testclient import TestClient
from fastapi import status
from .test_persistence import PromotionRepositoryDumb, PromotionRepositoryException
import src.main.web as web


API_BASIS = "/api/v1"
API_PROMOTIONS = f"{API_BASIS}/promotions"


class TestPromotionsEndpoint:
    """Test the promotions endpoint """
    def test_given_repository_when_get_promotions_then_get_200_and_promotions_list(self):
        web.repository = PromotionRepositoryDumb()
        client = TestClient(web.app)
        response = client.get(API_PROMOTIONS)
        assert response.status_code == status.HTTP_200_OK, response.text
        promotions_json = response.json()
        assert isinstance(promotions_json, list)
        assert len(promotions_json) >= 2
        for promotion_json in promotions_json:
            web.Promotion(**promotion_json)

    def test_given_repository_when_get_promotions_raises_exception_then_get_500(self):
        web.repository = PromotionRepositoryException()
        client = TestClient(web.app)
        response = client.get(API_PROMOTIONS)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR, response.text
