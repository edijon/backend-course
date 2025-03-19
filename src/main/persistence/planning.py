"""
This module defines the persistence layer for Planning and PlanningSlot entities.
It provides the SQLModel-based implementation for storing and retrieving planning-related
data from the database. The module includes the definition of Planning and PlanningSlot
tables, and a PlanningRepository class that offers CRUD operations and utility methods
for converting between domain and database representations of planning entities.
"""
from sqlmodel import Session, select, SQLModel, Field, Relationship
from typing import List
from datetime import date
from src.main.domain.planning import (
    IPlanningRepository, Planning as DomainPlanning, PlanningId, PlanningSlot as DomainPlanningSlot, PlanningSlotId)
from src.main.domain.base import BaseRepository
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
import uuid


class PlanningSlot(SQLModel, table=True):
    __tablename__ = "planning_slots"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hours_start: int
    minutes_start: int
    hours_end: int
    minutes_end: int
    promotion_id: str = Field(foreign_key="promotions.id")
    teacher_id: str = Field(foreign_key="teachers.id")
    course_id: str = Field(foreign_key="courses.id")
    room_id: str = Field(foreign_key="rooms.id")
    planning_id: str = Field(foreign_key="plannings.id")
    planning: "Planning" = Relationship(back_populates="slots")


class Planning(SQLModel, table=True):
    __tablename__ = "plannings"
    id: str = Field(primary_key=True)
    date: date
    promotion_id: str = Field(foreign_key="promotions.id")
    slots: List[PlanningSlot] = Relationship(back_populates="planning", cascade_delete=True)


class PlanningRepository(BaseRepository, IPlanningRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[DomainPlanning]:
        statement = select(Planning)
        results = self.session.exec(statement)
        return [self._to_domain(planning) for planning in results.all()]

    def find_by_id(self, id: PlanningId) -> DomainPlanning:
        statement = select(Planning).where(Planning.id == str(id))
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Planning not found")
        return self._to_domain(result)

    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[DomainPlanning]:
        statement = select(Planning).where(Planning.date == date, Planning.promotion_id == str(promotion_id))
        results = self.session.exec(statement)
        return [self._to_domain(planning) for planning in results.all()]

    def add(self, planning: DomainPlanning) -> None:
        planning_id = str(planning.id)
        db_planning = Planning(
            id=planning_id,
            date=planning.date,
            promotion_id=str(planning.promotion_id),
            slots=[self._to_db_slot(slot, planning_id) for slot in planning.slots]
        )
        self.session.add(db_planning)
        self.session.commit()

    def update(self, planning: DomainPlanning) -> None:
        planning_id = str(planning.id)
        db_planning = self.session.get(Planning, planning_id)
        if not db_planning:
            raise ValueError("Planning not found")
        db_planning.date = planning.date
        db_planning.promotion_id = str(planning.promotion_id)

        # Update existing slots and add new ones if necessary
        existing_slot_ids = {slot.id for slot in db_planning.slots}
        new_slot_ids = {slot.id for slot in planning.slots}

        # Delete slots that are no longer present
        for slot in db_planning.slots:
            if slot.id not in new_slot_ids:
                self.session.delete(slot)

        # Update or add slots
        for slot in planning.slots:
            if slot.id in existing_slot_ids:
                db_slot = self.session.get(PlanningSlot, slot.id)
                db_slot.hours_start = slot.hours_start
                db_slot.minutes_start = slot.minutes_start
                db_slot.hours_end = slot.hours_end
                db_slot.minutes_end = slot.minutes_end
                db_slot.teacher_id = str(slot.teacher_id)
                db_slot.course_id = str(slot.course_id)
                db_slot.room_id = str(slot.room_id)
            else:
                db_slot = self._to_db_slot(slot, planning_id)
                self.session.add(db_slot)

        self.session.commit()

    def delete(self, planning: DomainPlanning) -> None:
        planning_id = str(planning.id)
        db_planning = self.session.get(Planning, planning_id)
        if not db_planning:
            raise ValueError("Planning not found")
        self.session.delete(db_planning)
        self.session.commit()

    def _to_domain(self, planning: Planning) -> DomainPlanning:
        return DomainPlanning(
            id=PlanningId(id=planning.id),
            date=planning.date,
            promotion_id=PromotionId(id=planning.promotion_id),
            slots=[self._to_domain_slot(slot) for slot in planning.slots]
        )

    def _to_domain_slot(self, slot: PlanningSlot) -> DomainPlanningSlot:
        return DomainPlanningSlot(
            id=PlanningSlotId(id=slot.id),
            hours_start=slot.hours_start,
            minutes_start=slot.minutes_start,
            hours_end=slot.hours_end,
            minutes_end=slot.minutes_end,
            promotion_id=PromotionId(id=slot.promotion_id),
            teacher_id=TeacherId(id=slot.teacher_id),
            course_id=CourseId(id=slot.course_id),
            room_id=RoomId(id=slot.room_id)
        )

    def _to_db_slot(self, slot: DomainPlanningSlot, planning_id: str) -> PlanningSlot:
        return PlanningSlot(
            id=str(slot.id),
            hours_start=slot.hours_start,
            minutes_start=slot.minutes_start,
            hours_end=slot.hours_end,
            minutes_end=slot.minutes_end,
            promotion_id=str(slot.promotion_id),
            teacher_id=str(slot.teacher_id),
            course_id=str(slot.course_id),
            room_id=str(slot.room_id),
            planning_id=planning_id
        )

    def find_slot_by_id(self, planning_id: PlanningId, slot_id: PlanningSlotId) -> DomainPlanningSlot:
        statement = select(PlanningSlot).where(PlanningSlot.id == slot_id.id, PlanningSlot.planning_id == planning_id.id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Planning slot not found")
        return self._to_domain_slot(result)

    def add_slot(self, planning_id: PlanningId, slot: DomainPlanningSlot) -> None:
        db_slot = self._to_db_slot(slot)
        db_slot.planning_id = str(planning_id)
        self.session.add(db_slot)
        self.session.commit()

    def update_slot(self, planning_id: PlanningId, slot: DomainPlanningSlot) -> None:
        db_slot = self.session.get(PlanningSlot, str(slot.id))
        if not db_slot or db_slot.planning_id != str(planning_id):
            raise ValueError("Planning slot not found")
        db_slot.hours_start = slot.hours_start
        db_slot.minutes_start = slot.minutes_start
        db_slot.hours_end = slot.hours_end
        db_slot.minutes_end = slot.minutes_end
        db_slot.teacher_id = str(slot.teacher_id)
        db_slot.course_id = str(slot.course_id)
        db_slot.room_id = str(slot.room_id)
        self.session.add(db_slot)
        self.session.commit()

    def delete_slot(self, planning_id: PlanningId, slot_id: PlanningSlotId) -> None:
        db_slot = self.session.get(PlanningSlot, str(slot_id))
        if not db_slot or db_slot.planning_id != str(planning_id):
            raise ValueError("Planning slot not found")
        self.session.delete(db_slot)
        self.session.commit()
