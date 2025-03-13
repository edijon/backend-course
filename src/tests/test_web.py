from fastapi.testclient import TestClient
from fastapi import status
from .test_persistence import (
    PromotionRepositoryDumb, PromotionRepositoryException, PlanningRepositoryDumb,
    TeacherRepositoryDumb, CourseRepositoryDumb, RoomRepositoryDumb)
import src.main.web as web


API_BASIS = "/api/v1"
API_PROMOTIONS = f"{API_BASIS}/promotions"
API_PLANNING = f"{API_BASIS}/planning"
API_TOKEN = "/token"


client = TestClient(web.app)


def get_auth_token():
    response = client.post(API_TOKEN, data={"username": "user", "password": "password"})
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json()["access_token"]


def assert_response_status(response, expected_status):
    assert response.status_code == expected_status, response.text


def assert_promotion_list(promotions_json):
    assert isinstance(promotions_json, list)
    assert len(promotions_json) >= 2
    for promotion_json in promotions_json:
        web.Promotion(**promotion_json)


class TestPromotionsEndpoint:
    """Test the promotions endpoint """
    def setup_method(self):
        self.client = TestClient(web.app)

    def test_given_repository_when_get_promotions_then_get_200_and_promotions_list(self):
        web.repository_promotions = PromotionRepositoryDumb()
        response = self.client.get(API_PROMOTIONS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_promotion_list(response.json())

    def test_given_repository_when_get_promotions_raises_exception_then_get_500(self):
        web.repository_promotions = PromotionRepositoryException()
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


class TestPlanningEndpoint:
    """Test the planning endpoint """
    def setup_method(self):
        self.client = TestClient(web.app)

    def test_given_repository_when_get_planning_then_get_200_and_planning_ordered(self):
        web.repository_plannings = PlanningRepositoryDumb()
        web.repository_promotions = PromotionRepositoryDumb()  # Ensure correct repository is used
        web.repository_teachers = TeacherRepositoryDumb()  # Ensure correct repository is used
        web.repository_courses = CourseRepositoryDumb()  # Ensure correct repository is used
        web.repository_rooms = RoomRepositoryDumb()  # Ensure correct repository is used
        response = self.client.get(API_PLANNING)
        assert_response_status(response, status.HTTP_200_OK)
        planning_json = response.json()
        assert isinstance(planning_json, list)
        assert len(planning_json) >= 1
        self._assert_planning_ordered(planning_json)

    def test_given_valid_token_when_add_planning_then_get_200(self):
        token = get_auth_token()
        planning_data = {
            "id": "1",
            "slots": [
                {
                    "id": "1",
                    "date_start": "2021-09-01",
                    "hours_start": 9,
                    "minutes_start": 0,
                    "hours_end": 10,
                    "minutes_end": 0,
                    "promotion": {
                        "id": "1",
                        "study_year": 2,  # Provide study_year as an integer
                        "diploma": "DEUST",
                        "name": "Kempf"
                    },
                    "teacher": {
                        "id": "1",
                        "name": "Doe",
                        "firstname": "John"
                    },
                    "course": {
                        "id": "1",
                        "name": "Mathematics"
                    },
                    "room": {
                        "id": "1",
                        "name": "Room 101",
                        "description": "First floor room"
                    }
                }
            ]
        }
        response = self.client.post(API_PLANNING, json=planning_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == planning_data

    def test_given_invalid_token_when_add_planning_then_get_401(self):
        planning_data = {
            "id": "1",
            "slots": [
                {
                    "id": "1",
                    "date_start": "2021-09-01",
                    "hours_start": 9,
                    "minutes_start": 0,
                    "hours_end": 10,
                    "minutes_end": 0,
                    "promotion": {
                        "id": "1",
                        "study_year": 2,
                        "diploma": "DEUST",
                        "name": "Kempf"
                    },
                    "teacher": {
                        "id": "1",
                        "name": "Doe",
                        "firstname": "John"
                    },
                    "course": {
                        "id": "1",
                        "name": "Mathematics"
                    },
                    "room": {
                        "id": "1",
                        "name": "Room 101",
                        "description": "First floor room"
                    }
                }
            ]
        }
        response = self.client.post(API_PLANNING, json=planning_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def _assert_planning_ordered(self, planning_json):
        previous_date = None
        for planning in planning_json:
            self._assert_slots_ordered(planning['slots'], previous_date)

    def _assert_slots_ordered(self, slots, previous_date):
        previous_slot_time = None
        for slot in slots:
            current_date = slot['date_start']
            self._assert_date_order(current_date, previous_date)
            previous_date = current_date

            current_slot_time = (slot['hours_start'], slot['minutes_start'])
            self._assert_slot_time_order(current_slot_time, previous_slot_time)
            previous_slot_time = current_slot_time

    def _assert_date_order(self, current_date, previous_date):
        if previous_date is not None:
            assert current_date >= previous_date

    def _assert_slot_time_order(self, current_slot_time, previous_slot_time):
        if previous_slot_time is not None:
            assert current_slot_time >= previous_slot_time
