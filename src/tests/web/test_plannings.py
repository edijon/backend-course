from fastapi.testclient import TestClient
from fastapi import status
from src.tests.persistence import PlanningRepositoryDumb, PromotionRepositoryDumb, TeacherRepositoryDumb, CourseRepositoryDumb, RoomRepositoryDumb
from src.main.web.main import app
from src.main.web.planning import Planning, PlanningSlot, PlanningSlotWrite, PlanningWrite
from src.main.web.promotions import Promotion
from src.main.web import state
from datetime import date
import src.main.domain as domain
import uuid

# TODO: planning devrait utiliser promotion_id pas promotion

API_BASIS = "/api/v1"
API_PLANNINGS = f"{API_BASIS}/plannings"
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

def setup_module(module):
    state.repository_plannings = PlanningRepositoryDumb()
    state.repository_promotions = PromotionRepositoryDumb()
    state.repository_teachers = TeacherRepositoryDumb()
    state.repository_courses = CourseRepositoryDumb()
    state.repository_rooms = RoomRepositoryDumb()
    # Add initial data
    planning1 = domain.Planning(
        id=domain.PlanningId(id="1"),
        date=date(2023, 10, 10),
        promotion_id=domain.PromotionId(id="1"),
        slots=[]
    )
    planning2 = domain.Planning(
        id=domain.PlanningId(id="2"),
        date=date(2023, 10, 11),
        promotion_id=domain.PromotionId(id="2"),
        slots=[]
    )
    state.repository_plannings.save(planning1)
    state.repository_plannings.save(planning2)


def test_get_plannings():
    response = client.get(API_PLANNINGS)
    assert_response_status(response, status.HTTP_200_OK)
    assert_list_of_models(response.json(), Planning)

def test_add_planning():
    token = get_auth_token()
    planning_data = {
        "id": str(uuid.uuid4()),
        "date": "2023-10-12",
        "promotion_id": "1",
        "slots": []
    }
    response = client.post(API_PLANNINGS, json=planning_data, headers={"Authorization": f"Bearer {token}"})
    assert_response_status(response, status.HTTP_200_OK)
    assert response.json()["date"] == planning_data["date"]

def test_get_planning_by_id():
    response = client.get(f"{API_PLANNINGS}/1")
    assert_response_status(response, status.HTTP_200_OK)
    assert response.json()["id"] == "1"

def test_add_planning_slot():
    token = get_auth_token()
    slot_data = {
        "id": str(uuid.uuid4()),
        "hours_start": 9,
        "minutes_start": 0,
        "hours_end": 10,
        "minutes_end": 30,
        "promotion_id": "1",
        "teacher_id": "1",
        "course_id": "1",
        "room_id": "1"
    }
    response = client.post(f"{API_PLANNINGS}/1/slots", json=slot_data, headers={"Authorization": f"Bearer {token}"})
    assert_response_status(response, status.HTTP_200_OK)
    assert response.json()["slots"][0]["hours_start"] == slot_data["hours_start"]
