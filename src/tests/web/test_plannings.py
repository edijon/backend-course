from fastapi.testclient import TestClient
from fastapi import status
from typing import List
from src.tests.persistence import PlanningRepositoryDumb, PromotionRepositoryDumb, TeacherRepositoryDumb, CourseRepositoryDumb, RoomRepositoryDumb
from src.main.web.main import app
from src.main.web.planning import Planning

API_BASIS = "/api/v1"
API_PLANNING = f"{API_BASIS}/planning"
API_TOKEN = "/token"

client = TestClient(app)

def get_auth_token():
    response = client.post(API_TOKEN, data={"username": "user", "password": "password"})
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json()["access_token"]

def assert_response_status(response, expected_status):
    assert response.status_code == expected_status, response.text

class TestPlanningEndpoint:
    """Test the planning endpoint"""
    
    def setup_method(self):
        self.client = TestClient(app)

    def test_given_repository_when_get_planning_then_get_200_and_planning_ordered(self):
        self._setup_repositories()
        response = self.client.get(API_PLANNING)
        assert_response_status(response, status.HTTP_200_OK)
        planning_json = response.json()
        assert isinstance(planning_json, list)
        assert len(planning_json) >= 1
        self._assert_planning_ordered(planning_json)

    def test_given_date_and_promotion_id_when_get_planning_then_get_200_and_filtered_planning(self):
        self._setup_repositories()
        date = "2021-09-01"
        promotion_id = "1"
        response = self.client.get(f"{API_PLANNING}?date={date}&promotion_id={promotion_id}")
        assert_response_status(response, status.HTTP_200_OK)
        planning_json = response.json()
        assert isinstance(planning_json, list)
        assert len(planning_json) >= 1
        for planning in planning_json:
            assert planning["date"] == date
            assert planning["promotion"]["id"] == promotion_id

    def _setup_repositories(self):
        from src.main.web import state
        state.repository_plannings = PlanningRepositoryDumb()
        state.repository_promotions = PromotionRepositoryDumb()
        state.repository_teachers = TeacherRepositoryDumb()
        state.repository_courses = CourseRepositoryDumb()
        state.repository_rooms = RoomRepositoryDumb()

    def _assert_planning_ordered(self, planning_json: List[dict]):
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
