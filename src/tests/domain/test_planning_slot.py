from src.main.domain.planning import PlanningSlot, PlanningSlotId
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
import pytest


class TestPlanningSlot:
    """
    Test cases for PlanningSlot class. Even though in DDD, a PlanningSlot is manipulated via Planning,
    these tests verify the invariants of the entity during its creation.
    """
    @pytest.fixture
    def common_entities(self):
        return {
            "promotion_id": PromotionId(id="1"),
            "teacher_id": TeacherId(id="1"),
            "course_id": CourseId(id="1"),
            "room_id": RoomId(id="1")
        }

    def test_given_valid_times_and_entities_when_create_planning_slot_then_return_planning_slot(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 10
        minutes_end = 0
        # When
        planning_slot = PlanningSlot(
            id=planning_slot_id,
            hours_start=hours_start,
            minutes_start=minutes_start,
            hours_end=hours_end,
            minutes_end=minutes_end,
            **common_entities
        )
        # Then
        assert planning_slot.hours_start == hours_start
        assert planning_slot.minutes_start == minutes_start
        assert planning_slot.hours_end == hours_end
        assert planning_slot.minutes_end == minutes_end
        assert planning_slot.promotion_id == common_entities["promotion_id"]
        assert planning_slot.teacher_id == common_entities["teacher_id"]
        assert planning_slot.course_id == common_entities["course_id"]
        assert planning_slot.room_id == common_entities["room_id"]

    def test_given_invalid_end_time_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 10
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        # When/Then
        with pytest.raises(ValueError, match='End time must be after start time'):
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_duration_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 9
        minutes_end = 15
        # When/Then
        with pytest.raises(ValueError, match='Slot duration must be at least 30 minutes'):
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_duration_exceeds_four_hours_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 9
        minutes_start = 0
        hours_end = 13
        minutes_end = 1
        # When/Then
        with pytest.raises(ValueError, match='Slot duration must be at most 4 hours'):
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_start_time_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 8
        minutes_start = 0
        hours_end = 9
        minutes_end = 0
        # When/Then
        with pytest.raises(ValueError, match='First slot can only start at 08:15 or later'):
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )

    def test_given_invalid_end_time_limit_when_create_planning_slot_then_raise_value_error(self, common_entities):
        # Given
        planning_slot_id = PlanningSlotId(id="1")
        hours_start = 16
        minutes_start = 0
        hours_end = 17
        minutes_end = 30
        # When/Then
        with pytest.raises(ValueError, match='Last slot can only end at 17:15 or earlier'):
            PlanningSlot(
                id=planning_slot_id,
                hours_start=hours_start,
                minutes_start=minutes_start,
                hours_end=hours_end,
                minutes_end=minutes_end,
                **common_entities
            )
