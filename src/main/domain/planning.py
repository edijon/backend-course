"""
This module contains the definition of the Planning domain entity, which represents a planning for a promotion.
The Planning entity is an aggregate root that contains a list of PlanningSlot entities.
A PlanningSlot represents a course that takes place at a given hour in a given room.
"""
from typing import List
from abc import ABC, abstractmethod
from datetime import time, timedelta, date
from pydantic import BaseModel, Field, model_validator
from .base import BaseIdentifier
from .promotion import PromotionId
from .teacher import TeacherId
from .course import CourseId
from .room import RoomId


class PlanningSlotId(BaseIdentifier):
    """Value object holding PlanningSlot identity."""
    pass


class PlanningSlot(BaseModel):
    """
    PlanningSlot is an entity that holds the details of a planning slot.
    Note: This entity is part of the Planning aggregate and should only be managed via a Planning.
    Attributes:
        id (PlanningSlotId): Unique identifier for the planning slot.
        hours_start (int): Starting hour of the planning slot (must be between 8 and 17 inclusive).
        minutes_start (int): Starting minute of the planning slot (must be between 0 and 59 inclusive).
        hours_end (int): Ending hour of the planning slot (must be between 8 and 17 inclusive).
        minutes_end (int): Ending minute of the planning slot (must be between 0 and 59 inclusive).
        promotion_id (PromotionId): ID of the promotion associated with the planning slot.
        teacher_id (TeacherId): ID of the teacher assigned to the planning slot.
        course_id (CourseId): ID of the course associated with the planning slot.
        room_id (RoomId): ID of the room where the planning slot will take place.
    Validators:
        check_times: Ensures that the end time is after the start time, the duration is between 30 minutes and 4 hours,
                      the first slot starts at 08:15 or later, and the last slot ends at 17:15 or earlier.
    """
    id: PlanningSlotId
    hours_start: int = Field(..., ge=8, le=17)
    minutes_start: int = Field(..., ge=0, le=59)
    hours_end: int = Field(..., ge=8, le=17)
    minutes_end: int = Field(..., ge=0, le=59)
    promotion_id: PromotionId
    teacher_id: TeacherId
    course_id: CourseId
    room_id: RoomId

    @model_validator(mode="after")
    def check_times(self):
        start_time = time(self.hours_start, self.minutes_start)
        end_time = time(self.hours_end, self.minutes_end)
        if end_time <= start_time:
            raise ValueError("End time must be after start time")
        duration = timedelta(
            hours=end_time.hour, minutes=end_time.minute) - timedelta(hours=start_time.hour, minutes=start_time.minute)
        if duration < timedelta(minutes=30):
            raise ValueError("Slot duration must be at least 30 minutes")
        if duration > timedelta(hours=4):
            raise ValueError("Slot duration must be at most 4 hours")
        if self.hours_start == 8 and self.minutes_start < 15:
            raise ValueError("First slot can only start at 08:15 or later")
        if self.hours_end == 17 and self.minutes_end > 15:
            raise ValueError("Last slot can only end at 17:15 or earlier")
        return self


class PlanningId(BaseIdentifier):
    """Value object holding Planning identity."""
    pass


class Planning(BaseModel):
    """
    Aggregate root, entity holding planning.
    A Planning encapsulates a list of PlanningSlot. To respect the DDD, a PlanningSlot can only be
    manipulated through this aggregate.
    Attributes:
        id (PlanningId): Unique identifier for the planning.
        date (date): Date of the planning.
        promotion_id (PromotionId): ID of the promotion associated with the planning.
        slots (List[PlanningSlot]): List of planning slots.
    Validators:
        check_no_collisions: Ensures that there are no collisions between slots.
    """
    id: PlanningId
    date: date
    promotion_id: PromotionId
    slots: List[PlanningSlot]

    @model_validator(mode="after")
    def check_no_collisions(self):
        for i, slot1 in enumerate(self.slots):
            for j, slot2 in enumerate(self.slots):
                if i != j and self._slots_collide(slot1, slot2):
                    raise ValueError(f"Collision detected between slot {i+1} and slot {j+1}")
        return self

    def _slots_collide(self, slot1: PlanningSlot, slot2: PlanningSlot) -> bool:
        # Collisions occur if two slots of the same promotion, teacher, or room overlap.
        if slot1.promotion_id == slot2.promotion_id or slot1.teacher_id == slot2.teacher_id or slot1.room_id == slot2.room_id:
            start1 = time(slot1.hours_start, slot1.minutes_start)
            end1 = time(slot1.hours_end, slot1.minutes_end)
            start2 = time(slot2.hours_start, slot2.minutes_start)
            end2 = time(slot2.hours_end, slot2.minutes_end)
            return start1 < end2 and start2 < end1
        return False

    def add_slot(self, slot: PlanningSlot) -> None:
        """
        Adds a new slot to the planning after checking that it does not collide with any existing slots.
        """
        for existing in self.slots:
            if self._slots_collide(existing, slot):
                raise ValueError("Collision detected with an existing slot")
        self.slots.append(slot)
        self.check_no_collisions()

    def remove_slot(self, slot_id: PlanningSlotId) -> None:
        """
        Removes a slot from the planning given its identifier.
        """
        self.slots = [slot for slot in self.slots if slot.id != slot_id]
        self.check_no_collisions()

    def update_slot(self, updated_slot: PlanningSlot) -> None:
        """
        Updates an existing slot in the planning.
        """
        found = False
        new_slots = []
        for slot in self.slots:
            if slot.id == updated_slot.id:
                new_slots.append(updated_slot)
                found = True
            else:
                new_slots.append(slot)
        if not found:
            raise ValueError("Slot not found")
        # Ensure that the update does not cause any collision
        temp = self.model_copy(update={"slots": new_slots})
        temp.check_no_collisions()
        self.slots = new_slots


class IPlanningRepository(ABC):
    """Interface for handling plannings persistence."""
    @abstractmethod
    def next_identity(self) -> PlanningId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Planning]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: PlanningId) -> Planning:
        raise NotImplementedError

    @abstractmethod
    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[Planning]:
        raise NotImplementedError

    @abstractmethod
    def add(self, planning: Planning) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, planning: Planning) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, planning: Planning) -> None:
        raise NotImplementedError
