from typing import List
from datetime import date
import pytest
from sqlmodel import Session, create_engine, SQLModel
from src.main.domain.planning import Planning as DomainPlanning, PlanningId, PlanningSlot as DomainPlanningSlot, PlanningSlotId
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
from src.main.persistence.planning import PlanningRepository
import uuid


class PlanningRepositoryDumb:
    def __init__(self):
        self.plannings = []

    def next_identity(self) -> PlanningId:
        return PlanningId(id=str(len(self.plannings) + 1))

    def find_all(self) -> List[DomainPlanning]:
        return self.plannings

    def find_by_id(self, id: PlanningId) -> DomainPlanning:
        return next((planning for planning in self.plannings if str(planning.id) == str(id)), None)

    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[DomainPlanning]:
        return [planning for planning in self.plannings if planning.date == date and planning.promotion_id == promotion_id]

    def save(self, planning: DomainPlanning):
        for i, existing_planning in enumerate(self.plannings):
            if existing_planning.id == planning.id:
                self.plannings[i] = planning
                return
        self.plannings.append(planning)


class PlanningRepositoryException(PlanningRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def create_planning(repository, planning_id, promotion_id, planning_date, slots):
    planning = DomainPlanning(id=planning_id, date=planning_date, promotion_id=promotion_id, slots=slots)
    repository.add(planning)
    return planning


def test_planning_repository(session):
    repository = PlanningRepository(session)
    planning_id = PlanningId(id=repository.next_identity())
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    slots = [
        DomainPlanningSlot(
            id=PlanningSlotId(id=str(uuid.uuid4())),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=TeacherId(id="1"),
            course_id=CourseId(id="1"),
            room_id=RoomId(id="1")
        )
    ]
    planning = create_planning(repository, planning_id, promotion_id, planning_date, slots)

    assert planning.id is not None

    fetched_planning = repository.find_by_id(planning.id)
    assert fetched_planning is not None
    assert fetched_planning.date == planning_date

    fetched_planning.date = date(2023, 10, 11)
    repository.update(fetched_planning)
    updated_planning = repository.find_by_id(fetched_planning.id)
    assert updated_planning.date == date(2023, 10, 11)

    repository.delete(updated_planning)
    with pytest.raises(ValueError):
        repository.find_by_id(updated_planning.id)


def test_find_by_date_and_promotion(session):
    repository = PlanningRepository(session)
    planning_id = PlanningId(id=repository.next_identity())
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    slots = [
        DomainPlanningSlot(
            id=PlanningSlotId(id=str(uuid.uuid4())),
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=TeacherId(id="1"),
            course_id=CourseId(id="1"),
            room_id=RoomId(id="1")
        )
    ]
    create_planning(repository, planning_id, promotion_id, planning_date, slots)

    plannings = repository.find_by_date_and_promotion(planning_date, promotion_id)

    assert len(plannings) == 1
    assert plannings[0].id == planning_id


def test_planning_slot_relationship(session):
    repository = PlanningRepository(session)
    planning_id = PlanningId(id=repository.next_identity())
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    slot_id = PlanningSlotId(id=str(uuid.uuid4()))
    slots = [
        DomainPlanningSlot(
            id=slot_id,
            hours_start=9,
            minutes_start=0,
            hours_end=10,
            minutes_end=30,
            promotion_id=promotion_id,
            teacher_id=TeacherId(id="1"),
            course_id=CourseId(id="1"),
            room_id=RoomId(id="1")
        )
    ]
    create_planning(repository, planning_id, promotion_id, planning_date, slots)
    fetched_planning = repository.find_by_id(planning_id)
    assert len(fetched_planning.slots) == 1
    assert fetched_planning.slots[0].id == slot_id
