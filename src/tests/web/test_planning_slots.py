from fastapi.testclient import TestClient
from fastapi import status
from src.tests.persistence import PlanningRepositoryDumb, PlanningRepositoryException, PromotionRepositoryDumb, TeacherRepositoryDumb, CourseRepositoryDumb, RoomRepositoryDumb
from src.main.web.main import app
from src.main.web.planning import PlanningSlot

API_BASIS = "/api/v1"
API_PLANNING_SLOTS = f"{API_BASIS}/planning-slots"
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

class TestPlanningSlotsEndpoint:
    """Test the planning slots endpoint"""
    
    def setup_method(self):
        from src.main.web import state
        state.repository_promotions = PromotionRepositoryDumb()
        state.repository_teachers = TeacherRepositoryDumb()
        state.repository_courses = CourseRepositoryDumb()
        state.repository_rooms = RoomRepositoryDumb()
        self.client = TestClient(app)

    def test_given_repository_when_get_planning_slots_then_get_200_and_planning_slots_list(self):
        from src.main.web import state
        state.repository_plannings = PlanningRepositoryDumb()
        response = self.client.get(API_PLANNING_SLOTS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), PlanningSlot)

    def test_given_repository_when_get_planning_slots_raises_exception_then_get_500(self):
        from src.main.web import state
        state.repository_plannings = PlanningRepositoryException()
        response = self.client.get(API_PLANNING_SLOTS)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
