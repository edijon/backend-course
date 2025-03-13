from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import List
from pydantic import Field, model_validator
from datetime import time, timedelta, date


class BaseIdentifier(BaseModel):
    """Value object holding Component identity."""
    id: str
    model_config = ConfigDict(frozen=True)

    def __str__(self):
        return self.id


class PromotionId(BaseIdentifier):
    """Value object holding Promotion identity."""


class Promotion(BaseModel):
    """Aggregate root, entity holding promotion."""
    id: PromotionId
    study_year: int
    diploma: str
    name: str


class IPromotionRepository(ABC):
    """Interface for handling promotions persistence."""
    @abstractmethod
    def next_identity(self) -> PromotionId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Promotion]:
        raise NotImplementedError


class TeacherId(BaseIdentifier):
    """Value object holding Teacher identity."""


class Teacher(BaseModel):
    """Aggregate root, entity holding teacher."""
    id: TeacherId
    name: str
    firstname: str


class ITeacherRepository(ABC):
    """Interface for handling teachers persistence."""
    @abstractmethod
    def next_identity(self) -> TeacherId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Teacher]:
        raise NotImplementedError


class CourseId(BaseIdentifier):
    """Value object holding Course identity."""


class Course(BaseModel):
    """Aggregate root, entity holding course."""
    id: CourseId
    name: str


class ICourseRepository(ABC):
    """Interface for handling courses persistence."""
    @abstractmethod
    def next_identity(self) -> CourseId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Course]:
        raise NotImplementedError


class RoomId(BaseIdentifier):
    """Value object holding Room identity."""


class Room(BaseModel):
    """Aggregate root, entity holding room."""
    id: RoomId
    name: str
    description: str


class IRoomRepository(ABC):
    """Interface for handling rooms persistence."""
    @abstractmethod
    def next_identity(self) -> RoomId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Room]:
        raise NotImplementedError


class PlanningSlotId(BaseIdentifier):
    """Value object holding PlanningSlot identity."""


class PlanningSlot(BaseModel):
    """
    PlanningSlot is an aggregate root entity that holds the details of a planning slot.
    Attributes:
        id (PlanningSlotId): Unique identifier for the planning slot.
        date_start(date): Date of the planning slot.
        hours_start (int): Starting hour of the planning slot (must be between 8 and 17 inclusive).
        minutes_start (int): Starting minute of the planning slot (must be between 0 and 59 inclusive).
        hours_end (int): Ending hour of the planning slot (must be between 8 and 17 inclusive).
        minutes_end (int): Ending minute of the planning slot (must be between 0 and 59 inclusive).
        promotion (Promotion): Promotion associated with the planning slot.
        teacher (Teacher): Teacher assigned to the planning slot.
        course (Course): Course associated with the planning slot.
        room (Room): Room where the planning slot will take place.
    Validators:
        check_end_time: Ensures that the end time is after the start time.
        check_duration: Ensures that the duration of the slot is at least 30 minutes and at most 4 hours.
        check_start_time: Ensures that the first slot can only start at 08:15 or later.
        check_end_time_limit: Ensures that the last slot can only end at 17:15 or earlier.
    Note:
        The Field(..., ge=8, le=17) and similar constraints are used to enforce that the values are within the specified range.
    """
    id: PlanningSlotId
    date_start: date
    hours_start: int = Field(..., ge=8, le=17)
    minutes_start: int = Field(..., ge=0, le=59)
    hours_end: int = Field(..., ge=8, le=17)
    minutes_end: int = Field(..., ge=0, le=59)
    promotion: Promotion
    teacher: Teacher
    course: Course
    room: Room

    @model_validator(mode="after")
    def check_times(self):
        start_time = time(self.hours_start, self.minutes_start)
        end_time = time(self.hours_end, self.minutes_end)
        if end_time <= start_time:
            raise ValueError("End time must be after start time")
        duration = timedelta(
            hours=end_time.hour, minutes=end_time.minute
        ) - timedelta(hours=start_time.hour, minutes=start_time.minute)
        if duration < timedelta(minutes=30):
            raise ValueError("Slot duration must be at least 30 minutes")
        if duration > timedelta(hours=4):
            raise ValueError("Slot duration must be at most 4 hours")
        if self.hours_start == 8 and self.minutes_start < 15:
            raise ValueError("First slot can only start at 08:15 or later")
        if self.hours_end == 17 and self.minutes_end > 15:
            raise ValueError("Last slot can only end at 17:15 or earlier")
        return self


class IPlanningSlotRepository(ABC):
    """Interface for handling planning slots persistence."""
    @abstractmethod
    def next_identity(self) -> PlanningSlotId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[PlanningSlot]:
        raise NotImplementedError


class PlanningId(BaseIdentifier):
    """Value object holding Planning identity."""


class Planning(BaseModel):
    """
    Aggregate root, entity holding planning.
    Attributes:
        id (PlanningId): Unique identifier for the planning.
        slots (List[PlanningSlot]): List of planning slots.
    Validators:
        check_no_collisions: Ensures that there are no collisions between slots.
    """
    id: PlanningId
    slots: List[PlanningSlot]

    @model_validator(mode="after")
    def check_no_collisions(self):
        for i, slot1 in enumerate(self.slots):
            # This loop iterates over each slot in self.slots.
            # The enumerate function provides both the index (i) and the slot (slot1).
            for j, slot2 in enumerate(self.slots):
                if i != j and self._slots_collide(slot1, slot2):
                    raise ValueError(f"Collision detected between slot {i+1} and slot {j+1}")
        return self

    def _slots_collide(self, slot1: PlanningSlot, slot2: PlanningSlot) -> bool:
        if slot1.promotion == slot2.promotion or slot1.teacher == slot2.teacher or slot1.room == slot2.room:
            start1 = time(slot1.hours_start, slot1.minutes_start)
            end1 = time(slot1.hours_end, slot1.minutes_end)
            start2 = time(slot2.hours_start, slot2.minutes_start)
            end2 = time(slot2.hours_end, slot2.minutes_end)
            return start1 < end2 and start2 < end1
        return False


class IPlanningRepository(ABC):
    """Interface for handling plannings persistence."""
    @abstractmethod
    def next_identity(self) -> PlanningId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Planning]:
        raise NotImplementedError
