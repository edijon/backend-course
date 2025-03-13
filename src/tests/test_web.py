from fastapi.testclient import TestClient
from fastapi import status
from .test_persistence import (
    PromotionRepositoryDumb, PromotionRepositoryException, PlanningRepositoryDumb)
import src.main.web as web


API_BASIS = "/api/v1"
API_PROMOTIONS = f"{API_BASIS}/promotions"
API_PLANNING = f"{API_BASIS}/planning"


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



class TestPlanningEndpoint:
    """Test the planning endpoint """
    def test_given_repository_when_get_planning_then_get_200_and_planning_ordered(self):
        web.repository = PlanningRepositoryDumb()
        client = TestClient(web.app)
        response = client.get(API_PLANNING)
        assert response.status_code == status.HTTP_200_OK, response.text
        planning_json = response.json()
        assert isinstance(planning_json, list)
        assert len(planning_json) >= 1

        self._assert_planning_ordered(planning_json)

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
