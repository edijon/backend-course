from sqlmodel import Session, select, SQLModel, Field, Relationship, ForeignKey
from typing import List
from datetime import date
from src.main.domain.planning import IPlanningRepository, Planning as DomainPlanning, PlanningId, PlanningSlot as DomainPlanningSlot, PlanningSlotId
from src.main.domain.base import BaseRepository
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
import uuid


class PlanningSlot(SQLModel, table=True):
    __tablename__ = "planning_slots"
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    date_start: date
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
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    date: date
    promotion_id: str = Field(foreign_key="promotions.id")
    slots: List[PlanningSlot] = Relationship(back_populates="planning")


class PlanningRepository(BaseRepository, IPlanningRepository):
    def __init__(self, session: Session):
        self.session = session

    def next_identity(self) -> PlanningId:
        return PlanningId(id=str(uuid.uuid4()))

    def find_all(self) -> List[DomainPlanning]:
        statement = select(Planning)
        results = self.session.exec(statement)
        return [self._to_domain(planning) for planning in results.all()]

    def find_by_id(self, id: PlanningId) -> DomainPlanning:
        statement = select(Planning).where(Planning.id == id.id)
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Planning not found")
        return self._to_domain(result)

    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[DomainPlanning]:
        statement = select(Planning).where(Planning.date == date, Planning.promotion_id == promotion_id.id)
        results = self.session.exec(statement)
        return [self._to_domain(planning) for planning in results.all()]

    def find_all_slots(self) -> List[DomainPlanningSlot]:
        statement = select(PlanningSlot)
        results = self.session.exec(statement)
        return [self._to_domain_slot(slot) for slot in results.all()]

    def add(self, planning: DomainPlanning) -> None:
        db_planning = Planning(
            id=planning.id.id,
            date=planning.date,
            promotion_id=planning.promotion_id.id,
            slots=[self._to_db_slot(slot) for slot in planning.slots]
        )
        self.session.add(db_planning)
        self.session.commit()

    def update(self, planning: DomainPlanning) -> None:
        db_planning = Planning(
            id=planning.id.id,
            date=planning.date,
            promotion_id=planning.promotion_id.id,
            slots=[self._to_db_slot(slot) for slot in planning.slots]
        )
        self.session.merge(db_planning)
        self.session.commit()

    def delete(self, id: PlanningId) -> None:
        planning = self.find_by_id(id)
        db_planning = self.session.get(Planning, id.id)
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
            date_start=slot.date_start,
            hours_start=slot.hours_start,
            minutes_start=slot.minutes_start,
            hours_end=slot.hours_end,
            minutes_end=slot.minutes_end,
            promotion_id=PromotionId(id=slot.promotion_id),
            teacher_id=TeacherId(id=slot.teacher_id),
            course_id=CourseId(id=slot.course_id),
            room_id=RoomId(id=slot.room_id),
            planning_id=PlanningId(id=slot.planning_id)
        )

    def _to_db_slot(self, slot: DomainPlanningSlot) -> PlanningSlot:
        return PlanningSlot(
            id=slot.id.id,
            date_start=slot.date_start,
            hours_start=slot.hours_start,
            minutes_start=slot.minutes_start,
            hours_end=slot.hours_end,
            minutes_end=slot.minutes_end,
            promotion_id=slot.promotion_id.id,
            teacher_id=slot.teacher_id.id,
            course_id=slot.course_id.id,
            room_id=slot.room_id.id,
            planning_id=slot.planning_id.id
        )