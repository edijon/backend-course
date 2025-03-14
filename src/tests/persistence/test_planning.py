from src.main.domain import (
    BaseRepository, IPlanningRepository, Planning, PlanningId,
    PlanningSlot, PlanningSlotId, PromotionId, TeacherId, CourseId, RoomId
)
from datetime import date
from typing import List
from sqlmodel import Session, create_engine, SQLModel
from src.main.persistence.planning import Planning as DBPlanning, PlanningSlot as DBPlanningSlot, PlanningRepository
import pytest

class PlanningRepositoryDumb(BaseRepository, IPlanningRepository):
    """Dumb implementation of IPlanningRepository."""
    def __init__(self):
        self.plannings = [
            Planning(
                id=PlanningId(id="1"),
                date=date(2021, 9, 1),
                promotion_id=PromotionId(id="1"),
                slots=self._create_slots()
            )
        ]

    def _create_slots(self):
        return [
            PlanningSlot(
                id=PlanningSlotId(id="1"),
                date_start=date(2021, 9, 1),
                hours_start=9,
                minutes_start=0,
                hours_end=10,
                minutes_end=0,
                promotion_id=PromotionId(id="1"),
                teacher_id=TeacherId(id="1"),
                course_id=CourseId(id="1"),
                room_id=RoomId(id="1"),
                planning_id=PlanningId(id="1")
            ),
            PlanningSlot(
                id=PlanningSlotId(id="2"),
                date_start=date(2021, 9, 1),
                hours_start=10,
                minutes_start=15,
                hours_end=11,
                minutes_end=15,
                promotion_id=PromotionId(id="2"),
                teacher_id=TeacherId(id="2"),
                course_id=CourseId(id="2"),
                room_id=RoomId(id="2"),
                planning_id=PlanningId(id="1")
            )
        ]

    def find_all(self):
        return self.plannings

    def find_by_id(self, id: PlanningId):
        for planning in self.plannings:
            if planning.id == id:
                return planning
        raise ValueError("Planning not found")

    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[Planning]:
        return [planning for planning in self.plannings if planning.date == date and planning.promotion_id == promotion_id]

    def find_all_slots(self):
        slots = []
        for planning in self.plannings:
            slots.extend(planning.slots)
        return slots

class PlanningRepositoryException(PlanningRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: PlanningId):
        raise Exception("Test exception")

    def find_all_slots(self):
        raise Exception("Test exception")
