from src.main.domain.planning import Planning, PlanningId, PlanningSlot, PlanningSlotId
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
from datetime import date
import pytest


class TestPlanning:
    """Test cases for Planning aggregate and its slot management methods."""
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

    @pytest.fixture
    def empty_planning(self, common_entities):
        planning_id = PlanningId(id="1")
        slots = []
        return Planning(id=planning_id, date=date(2021, 9, 1), promotion_id=common_entities["promotion1"], slots=slots)

    def create_slot(self, slot_id: str, start_hour: int, start_min: int, end_hour: int, end_min: int, common_entities,
                    promo_key="promotion1", teacher_key="teacher1", course_key="course1", room_key="room1"):
        return PlanningSlot(
            id=PlanningSlotId(id=slot_id),
            hours_start=start_hour,
            minutes_start=start_min,
            hours_end=end_hour,
            minutes_end=end_min,
            promotion_id=common_entities[promo_key],
            teacher_id=common_entities[teacher_key],
            course_id=common_entities[course_key],
            room_id=common_entities[room_key]
        )

    def test_given_valid_slots_in_constructor_when_create_planning_then_return_planning(self, common_entities):
        # Given
        planning_id = PlanningId(id="1")
        date_planning = date(2021, 9, 1)
        promotion_id = common_entities["promotion1"]
        slot1 = self.create_slot("1", 9, 0, 10, 0, common_entities)
        slot2 = self.create_slot("2", 10, 15, 11, 15, common_entities, promo_key="promotion2", teacher_key="teacher2",
                                 course_key="course2", room_key="room2")
        # When
        planning = Planning(id=planning_id, date=date_planning, promotion_id=promotion_id, slots=[slot1, slot2])
        # Then
        assert planning.id == planning_id
        assert planning.date == date_planning
        assert planning.promotion_id == promotion_id
        assert len(planning.slots) == 2

    def test_add_valid_slot_to_planning(self, empty_planning, common_entities):
        # Given
        slot = self.create_slot("1", 9, 0, 10, 0, common_entities)
        # When
        empty_planning.add_slot(slot)
        # Then
        assert len(empty_planning.slots) == 1
        assert empty_planning.slots[0] == slot

    def test_add_colliding_slot_to_planning_then_raise_value_error(self, empty_planning, common_entities):
        # Given
        slot1 = self.create_slot("1", 9, 0, 10, 0, common_entities)
        slot2 = self.create_slot("2", 9, 30, 10, 30, common_entities)
        empty_planning.add_slot(slot1)
        # When/Then
        with pytest.raises(ValueError, match="Collision detected"):
            empty_planning.add_slot(slot2)

    def test_remove_slot_from_planning(self, empty_planning, common_entities):
        # Given
        slot1 = self.create_slot("1", 9, 0, 10, 0, common_entities)
        slot2 = self.create_slot("2", 10, 15, 11, 15, common_entities, promo_key="promotion2", teacher_key="teacher2",
                                 course_key="course2", room_key="room2")
        empty_planning.add_slot(slot1)
        empty_planning.add_slot(slot2)
        # When
        empty_planning.remove_slot(slot1.id)
        # Then
        assert len(empty_planning.slots) == 1
        assert empty_planning.slots[0] == slot2

    def test_update_slot_in_planning_successfully(self, empty_planning, common_entities):
        # Given
        slot = self.create_slot("1", 9, 0, 10, 0, common_entities)
        empty_planning.add_slot(slot)
        # When: updating the slot to shift the schedule (without collision)
        updated_slot = self.create_slot("1", 10, 0, 11, 0, common_entities)
        empty_planning.update_slot(updated_slot)
        # Then
        assert empty_planning.slots[0].hours_start == 10
        assert empty_planning.slots[0].hours_end == 11

    def test_update_slot_in_planning_with_collision_then_raise_value_error(self, empty_planning, common_entities):
        # Given
        slot1 = self.create_slot("1", 9, 0, 10, 0, common_entities)
        # Here, the initial slot2 is without collision (different teacher, promotion, etc.)
        slot2 = self.create_slot("2", 10, 15, 11, 15, common_entities, promo_key="promotion2", teacher_key="teacher2",
                                 course_key="course2", room_key="room2")
        empty_planning.add_slot(slot1)
        empty_planning.add_slot(slot2)
        # When: updating slot2 to create a collision with slot1
        # To cause the collision, we force slot2 to share the same teacher as slot1.
        updated_slot2 = self.create_slot("2", 9, 30, 10, 30, common_entities, promo_key="promotion2", teacher_key="teacher1",
                                         course_key="course2", room_key="room2")
        with pytest.raises(ValueError, match="Collision detected"):
            empty_planning.update_slot(updated_slot2)

    def test_update_nonexistent_slot_then_raise_value_error(self, empty_planning, common_entities):
        # Given
        slot = self.create_slot("1", 9, 0, 10, 0, common_entities)
        # When/Then
        with pytest.raises(ValueError, match="Slot not found"):
            empty_planning.update_slot(slot)
