from src.main.domain import (
    Promotion, PromotionId, Teacher, TeacherId, Course, CourseId, Room, RoomId,
    PlanningSlot, PlanningSlotId, Planning, PlanningId)
from datetime import date
import pytest


class TestPromotion:
    """Test cases for Promotion class."""

    def test_given_study_year_and_diploma_and_name_when_create_promotion_then_return_promotion(self):
        # Given
        promotion_id = PromotionId(id="1")
        study_year = 2
        diploma = "DEUST"
        name = "Kempf"
        # When
        promotion = Promotion(id=promotion_id, study_year=study_year, diploma=diploma, name=name)
        # Then
        assert promotion.study_year == study_year
        assert promotion.diploma == diploma
        assert promotion.name == name


class TestTeacher:
    """Test cases for Teacher class."""

    def test_given_name_and_firstname_when_create_teacher_then_return_teacher(self):
        # Given
        teacher_id = TeacherId(id="1")
        name = "Doe"
        firstname = "John"
        # When
        teacher = Teacher(id=teacher_id, name=name, firstname=firstname)
        # Then
        assert teacher.name == name
        assert teacher.firstname == firstname


class TestCourse:
    """Test cases for Course class."""

    def test_given_name_when_create_course_then_return_course(self):
        # Given
        course_id = CourseId(id="1")
        name = "Mathematics"
        # When
        course = Course(id=course_id, name=name)
        # Then
        assert course.name == name


class TestRoom:
    """Test cases for Room class."""

    def test_given_name_and_description_when_create_room_then_return_room(self):
        # Given
        room_id = RoomId(id="1")
        name = "Room 101"
        description = "First floor room"
        # When
        room = Room(id=room_id, name=name, description=description)
        # Then
        assert room.name == name
        assert room.description == description


class TestPlanningSlot:
    """Test cases for PlanningSlot class."""

    @pytest.fixture
    def common_entities(self):
        return {
            "promotion": Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf"),
            "teacher": Teacher(id=TeacherId(id="1"), name="Doe", firstname="John"),
            "course": Course(id=CourseId(id="1"), name="Mathematics"),
            "room": Room(id=RoomId(id="1"), name="Room 101", description="First floor room")
        }

    def test_given_valid_times_and_entities_when_create_planning_slot_then_return_planning_slot(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 9
        minutes_start = 0
        hours_end = 10
        minutes_end = 0
        # When
        planning_slot = PlanningSlot(
            id=planning_slot_id,
            date_start=date_start,
            hours_start=hours_start,
            minutes_start=minutes_start,
            hours_end=hours_end,
            minutes_end=minutes_end,
            **common_entities
        )
        # Then
        assert planning_slot.date_start == date.fromisoformat(date_start)
        assert planning_slot.hours_start == hours_start
        assert planning_slot.minutes_start == minutes_start
        assert planning_slot.hours_end == hours_end
        assert planning_slot.minutes_end == minutes_end
        assert planning_slot.promotion == common_entities["promotion"]
        assert planning_slot.teacher == common_entities["teacher"]
        assert planning_slot.course == common_entities["course"]
        assert planning_slot.room == common_entities["room"]

    def test_given_invalid_end_time_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 10
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        # When/Then
        with pytest.raises(ValueError, match='End time must be after start time'):
            PlanningSlot(
                id=planning_slot_id,
                date_start=date_start,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_duration_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 9
        minutes_start = 0
        hours_end = 9
        minutes_end = 15
        # When/Then
        with pytest.raises(ValueError, match='Slot duration must be at least 30 minutes'):
            PlanningSlot(
                id=planning_slot_id,
                date_start=date_start,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_duration_exceeds_four_hours_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 9
        minutes_start = 0
        hours_end = 13
        minutes_end = 1
        # When/Then
        with pytest.raises(ValueError, match='Slot duration must be at most 4 hours'):
            PlanningSlot(
                id=planning_slot_id,
                date_start=date_start,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_start_time_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 8
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        # When/Then
        with pytest.raises(ValueError, match='First slot can only start at 08:15 or later'):
            PlanningSlot(
                id=planning_slot_id,
                date_start=date_start,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_end_time_limit_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        date_start = "2021-09-01"
        hours_start = 16
        minutes_start = 0
        hours_end = 17
        minutes_end = 30
        # When/Then
        with pytest.raises(ValueError, match='Last slot can only end at 17:15 or earlier'):
            PlanningSlot(
                id=planning_slot_id,
                date_start=date_start,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )


class TestPlanning:
    """Test cases for Planning class."""

    @pytest.fixture
    def common_entities(self):
        return {
            "promotion1": Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf"),
            "promotion2": Promotion(id=PromotionId(id="2"), study_year=3, diploma="DEUST", name="Smith"),
            "teacher1": Teacher(id=TeacherId(id="1"), name="Doe", firstname="John"),
            "teacher2": Teacher(id=TeacherId(id="2"), name="Brown", firstname="Alice"),
            "course1": Course(id=CourseId(id="1"), name="Mathematics"),
            "course2": Course(id=CourseId(id="2"), name="Physics"),
            "room1": Room(id=RoomId(id="1"), name="Room 101", description="First floor room"),
            "room2": Room(id=RoomId(id="2"), name="Room 102", description="Second floor room")
        }

    def test_given_valid_slots_when_create_planning_then_return_planning(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=10,
            minutes_start=15,
            hours_end=11,
            minutes_end=15,
            promotion=common_entities["promotion2"],
            teacher=common_entities["teacher2"],
            course=common_entities["course2"],
            room=common_entities["room2"]
        )
        # When
        planning = Planning(id=planning_id, slots=[slot1, slot2])
        # Then
        assert planning.id == planning_id
        assert len(planning.slots) == 2

    def test_given_colliding_slots_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, slots=[slot1, slot2])

    def test_given_valid_slots_with_different_promotions_teachers_rooms_when_create_planning_then_return_planning(
            self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion2"],
            teacher=common_entities["teacher2"],
            course=common_entities["course2"],
            room=common_entities["room2"]
        )
        # When
        planning = Planning(id=planning_id, slots=[slot1, slot2])
        # Then
        assert planning.id == planning_id
        assert len(planning.slots) == 2

    def test_given_slots_with_same_teacher_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion=common_entities["promotion2"],
            teacher=common_entities["teacher1"],
            course=common_entities["course2"],
            room=common_entities["room2"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, slots=[slot1, slot2])

    def test_given_slots_with_same_room_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion=common_entities["promotion2"],
            teacher=common_entities["teacher2"],
            course=common_entities["course2"],
            room=common_entities["room1"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, slots=[slot1, slot2])

    def test_given_slots_with_same_promotion_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher1"],
            course=common_entities["course1"],
            room=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start="2021-09-01",
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion=common_entities["promotion1"],
            teacher=common_entities["teacher2"],
            course=common_entities["course2"],
            room=common_entities["room2"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, slots=[slot1, slot2])
