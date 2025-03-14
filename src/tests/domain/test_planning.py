from src.main.domain.planning import Planning, PlanningId, PlanningSlot, PlanningSlotId
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
from datetime import date
import pytest

class TestPlanning:
    """Test cases for Planning class."""
    
    @pytest.fixture
    def common_entities(self):
        return {
            "promotion1": PromotionId(id="1"),
            "promotion2": PromotionId(id="2"),
            "teacher1": TeacherId(id="1"),
            "teacher2": TeacherId(id="2"),
            "course1": CourseId(id="1"),
            "course2": CourseId(id="2"),
            "room1": RoomId(id="1"),
            "room2": RoomId(id="2")
        }

    def test_given_valid_slots_when_create_planning_then_return_planning(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=10,
            minutes_start=15,
            hours_end=11,
            minutes_end=15,
            promotion_id=common_entities["promotion2"],
            teacher_id=common_entities["teacher2"],
            course_id=common_entities["course2"],
            room_id=common_entities["room2"]
        )
        # When
        planning = Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])
        # Then
        assert planning.id == planning_id
        assert planning.date == date_planning
        assert planning.promotion_id == promotion_id
        assert len(planning.slots) == 2

    def test_given_colliding_slots_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])

    def test_given_valid_slots_with_different_promotions_teachers_rooms_when_create_planning_then_return_planning(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=common_entities["promotion2"],
            teacher_id=common_entities["teacher2"],
            course_id=common_entities["course2"],
            room_id=common_entities["room2"]
        )
        # When
        planning = Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])
        # Then
        assert planning.id == planning_id
        assert planning.date == date_planning
        assert planning.promotion_id == promotion_id
        assert len(planning.slots) == 2

    def test_given_slots_with_same_teacher_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course2"],
            room_id=common_entities["room2"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])

    def test_given_slots_with_same_room_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher2"],
            course_id=common_entities["course2"],
            room_id=common_entities["room1"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])

    def test_given_slots_with_same_promotion_when_create_planning_then_raise_value_error(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = PlanningSlot(
            id=PlanningSlotId(id="1"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=0,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher1"],
            course_id=common_entities["course1"],
            room_id=common_entities["room1"]
        )
        slot2 = PlanningSlot(
            id=PlanningSlotId(id="2"),
            date_start=date(2021, 9, 1),
            hours_start=9,
            minutes_start=30,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=common_entities["teacher2"],
            course_id=common_entities["course2"],
            room_id=common_entities["room2"]
        )
        # When/Then
        with pytest.raises(ValueError, match='Collision detected between slot 1 and slot 2'):
            Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])
