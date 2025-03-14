from fastapi.testclient import TestClient
from fastapi import status
from typing import List
from .test_persistence import (
    PromotionRepositoryDumb, PromotionRepositoryException, PlanningRepositoryDumb,
    TeacherRepositoryDumb, TeacherRepositoryException, CourseRepositoryDumb, CourseRepositoryException, RoomRepositoryDumb,
    RoomRepositoryException, PlanningRepositoryException)
import src.main.web as web

API_BASIS = "/api/v1"
API_PROMOTIONS = f"{API_BASIS}/promotions"
API_PLANNING = f"{API_BASIS}/planning"
API_COURSES = f"{API_BASIS}/courses"
API_TEACHERS = f"{API_BASIS}/teachers"
API_ROOMS = f"{API_BASIS}/rooms"
API_PLANNING_SLOTS = f"{API_BASIS}/planning-slots"
API_TOKEN = "/token"

client = TestClient(web.app)

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
        self.client = TestClient(web.app)

    def test_given_repository_when_get_promotions_then_get_200_and_promotions_list(self):
        web.repository_promotions = PromotionRepositoryDumb()
        response = self.client.get(API_PROMOTIONS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), web.Promotion)

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

class TestTeachersEndpoint:
    """Test the teachers endpoint"""
    
    def setup_method(self):
        self.client = TestClient(web.app)

    def test_given_repository_when_get_teachers_then_get_200_and_teachers_list(self):
        web.repository_teachers = TeacherRepositoryDumb()
        response = self.client.get(API_TEACHERS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), web.Teacher)

    def test_given_repository_when_get_teachers_raises_exception_then_get_500(self):
        web.repository_teachers = TeacherRepositoryException()
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

class TestCoursesEndpoint:
    """Test the courses endpoint"""
    
    def setup_method(self):
        self.client = TestClient(web.app)

    def test_given_repository_when_get_courses_then_get_200_and_courses_list(self):
        web.repository_courses = CourseRepositoryDumb()
        response = self.client.get(API_COURSES)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), web.Course)

    def test_given_repository_when_get_courses_raises_exception_then_get_500(self):
        web.repository_courses = CourseRepositoryException()
        response = self.client.get(API_COURSES)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_given_valid_token_when_add_course_then_get_200(self):
        token = get_auth_token()
        course_data = {
            "id": "1",
            "name": "Mathematics"
        }
        response = self.client.post(API_COURSES, json=course_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == course_data

    def test_given_invalid_token_when_add_course_then_get_401(self):
        course_data = {
            "id": "1",
            "name": "Mathematics"
        }
        response = self.client.post(API_COURSES, json=course_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_update_course_then_get_200(self):
        token = get_auth_token()
        course_data = {
            "id": "1",
            "name": "Mathematics"
        }
        response = self.client.put(f"{API_COURSES}/1", json=course_data, headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == course_data

    def test_given_invalid_token_when_update_course_then_get_401(self):
        course_data = {
            "id": "1",
            "name": "Mathematics"
        }
        response = self.client.put(f"{API_COURSES}/1", json=course_data, headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

    def test_given_valid_token_when_delete_course_then_get_200(self):
        token = get_auth_token()
        response = self.client.delete(f"{API_COURSES}/1", headers={"Authorization": f"Bearer {token}"})
        assert_response_status(response, status.HTTP_200_OK)
        assert response.json() == {"message": "Course deleted"}

    def test_given_invalid_token_when_delete_course_then_get_401(self):
        response = self.client.delete(f"{API_COURSES}/1", headers={"Authorization": "Bearer invalid-token"})
        assert_response_status(response, status.HTTP_401_UNAUTHORIZED)

class TestRoomsEndpoint:
    """Test the rooms endpoint"""
    
    def setup_method(self):
        self.client = TestClient(web.app)

    def test_given_repository_when_get_rooms_then_get_200_and_rooms_list(self):
        web.repository_rooms = RoomRepositoryDumb()
        response = self.client.get(API_ROOMS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), web.Room)

    def test_given_repository_when_get_rooms_raises_exception_then_get_500(self):
        web.repository_rooms = RoomRepositoryException()
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

class TestPlanningSlotsEndpoint:
    """Test the planning slots endpoint"""
    
    def setup_method(self):
        web.repository_promotions = PromotionRepositoryDumb()
        web.repository_teachers = TeacherRepositoryDumb()
        web.repository_courses = CourseRepositoryDumb()
        web.repository_rooms = RoomRepositoryDumb()
        self.client = TestClient(web.app)

    def test_given_repository_when_get_planning_slots_then_get_200_and_planning_slots_list(self):
        web.repository_plannings = PlanningRepositoryDumb()
        response = self.client.get(API_PLANNING_SLOTS)
        assert_response_status(response, status.HTTP_200_OK)
        assert_list_of_models(response.json(), web.PlanningSlot)

    def test_given_repository_when_get_planning_slots_raises_exception_then_get_500(self):
        web.repository_plannings = PlanningRepositoryException()
        response = self.client.get(API_PLANNING_SLOTS)
        assert_response_status(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

class TestPlanningEndpoint:
    """Test the planning endpoint"""
    
    def setup_method(self):
        self.client = TestClient(web.app)

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
        web.repository_plannings = PlanningRepositoryDumb()
        web.repository_promotions = PromotionRepositoryDumb()
        web.repository_teachers = TeacherRepositoryDumb()
        web.repository_courses = CourseRepositoryDumb()
        web.repository_rooms = RoomRepositoryDumb()

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
