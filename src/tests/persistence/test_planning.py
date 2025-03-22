import uuid
from datetime import date
from typing import List
import pytest
from sqlmodel import Session, create_engine, SQLModel

from src.main.domain.planning import (
    IPlanningRepository, Planning as DomainPlanning, PlanningId, PlanningSlot as DomainPlanningSlot, PlanningSlotId)
from src.main.domain.promotion import PromotionId
from src.main.domain.teacher import TeacherId
from src.main.domain.course import CourseId
from src.main.domain.room import RoomId
from src.main.persistence.planning import PlanningRepository, Planning, PlanningSlot


class PlanningRepositoryDumb(IPlanningRepository):
    def __init__(self):
        self.plannings = []

    def next_identity(self) -> PlanningId:
        return PlanningId(id=str(len(self.plannings) + 1))

    def find_all(self) -> List[DomainPlanning]:
        return self.plannings

    def find_by_id(self, id: PlanningId) -> DomainPlanning:
        return next((p for p in self.plannings if str(p.id) == str(id)), None)

    def find_by_date_and_promotion(self, date: date, promotion_id: PromotionId) -> List[DomainPlanning]:
        return [p for p in self.plannings if p.date == date and p.promotion_id == promotion_id]

    def add(self, planning: DomainPlanning):
        for i, existing in enumerate(self.plannings):
            if existing.id == planning.id:
                self.plannings[i] = planning
                return
        self.plannings.append(planning)

    def delete(self, planning: DomainPlanning):
        self.plannings = [p for p in self.plannings if p.id != planning.id]

    def update(self, planning: DomainPlanning):
        for i, existing in enumerate(self.plannings):
            if existing.id == planning.id:
                self.plannings[i] = planning
                return
        raise ValueError("Planning not found")


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


def create_domain_slot(slot_id: str = None) -> DomainPlanningSlot:
    return DomainPlanningSlot(
        id=PlanningSlotId(id=slot_id or str(uuid.uuid4())),
        hours_start=9,
        minutes_start=0,
        hours_end=10,
        minutes_end=30,
        promotion_id=PromotionId(id="1"),
        teacher_id=TeacherId(id="1"),
        course_id=CourseId(id="1"),
        room_id=RoomId(id="1")
    )


def create_planning(repository, planning_id, promotion_id, planning_date, slots):
    planning = DomainPlanning(id=planning_id, date=planning_date, promotion_id=promotion_id, slots=slots)
    repository.add(planning)
    return planning


# ===================== TESTS ========================

def test_empty_database_when_find_by_id_then_raise_exception(session):
    repo = PlanningRepository(session)
    with pytest.raises(ValueError):
        repo.find_by_id(PlanningId(id="nonexistent"))


def test_existing_planning_when_find_by_id_then_return_planning(session):
    repo = PlanningRepository(session)
    planning_id = PlanningId(id=str(uuid.uuid4()))
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    slot = create_domain_slot()
    create_planning(repo, planning_id, promotion_id, planning_date, [slot])

    fetched = repo.find_by_id(planning_id)
    assert fetched.id == planning_id
    assert fetched.date == planning_date
    assert len(fetched.slots) == 1


def test_existing_planning_when_update_date_then_date_is_updated(session):
    repo = PlanningRepository(session)
    db_planning = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[])
    repo.add(repo._to_domain(db_planning))

    new_date = date(2022, 1, 2)
    new_promotion = "2"
    updated = DomainPlanning(id=PlanningId(id="1"), date=new_date, promotion_id=PromotionId(id=new_promotion), slots=[])
    repo._update_planning(db_planning, updated)

    assert db_planning.date == new_date
    assert db_planning.promotion_id == new_promotion


def test_existing_planning_with_slot_when_slot_removed_then_slot_is_deleted(session):
    repo = PlanningRepository(session)
    slot = PlanningSlot(
        id="1", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="1"
    )
    db_planning = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[slot])
    session.add(db_planning)
    session.commit()

    assert len(db_planning.slots) == 1

    updated = DomainPlanning(id=PlanningId(id="1"), date=db_planning.date, promotion_id=PromotionId(id="1"), slots=[])
    repo._update_planning(db_planning, updated)

    assert len(db_planning.slots) == 0


def test_existing_slot_when_updated_then_slot_fields_are_updated(session):
    repo = PlanningRepository(session)
    slot = PlanningSlot(
        id="1", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="1"
    )
    db_planning = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[slot])
    session.add(db_planning)
    session.commit()

    updated_slot = DomainPlanningSlot(
        id=PlanningSlotId(id="1"), hours_start=10, minutes_start=5, hours_end=11, minutes_end=10,
        promotion_id=PromotionId(id="1"), teacher_id=TeacherId(id="1"),
        course_id=CourseId(id="1"), room_id=RoomId(id="1")
    )
    updated = DomainPlanning(
        id=PlanningId(id="1"), date=db_planning.date, promotion_id=PromotionId(id="1"), slots=[updated_slot])
    repo._update_planning(db_planning, updated)

    assert slot.hours_start == 10
    assert slot.minutes_start == 5
    assert slot.hours_end == 11
    assert slot.minutes_end == 10


def test_empty_planning_when_new_slot_added_then_slot_is_created(session):
    repo = PlanningRepository(session)
    db_planning = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[])
    session.add(db_planning)
    session.commit()

    domain_slot = create_domain_slot(slot_id="1")
    updated = DomainPlanning(
        id=PlanningId(id="1"), date=db_planning.date, promotion_id=PromotionId(id="1"), slots=[domain_slot])
    repo._update_planning(db_planning, updated)

    assert len(db_planning.slots) == 1


def test_existing_planning_when_deleted_then_not_found(session):
    repo = PlanningRepository(session)
    planning_id = PlanningId(id=str(uuid.uuid4()))
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    create_planning(repo, planning_id, promotion_id, planning_date, [])

    repo.delete(DomainPlanning(id=planning_id, date=planning_date, promotion_id=promotion_id, slots=[]))

    with pytest.raises(ValueError):
        repo.find_by_id(planning_id)


def test_existing_planning_when_find_by_date_and_promotion_then_return_planning(session):
    repo = PlanningRepository(session)
    planning_id = PlanningId(id=str(uuid.uuid4()))
    promotion_id = PromotionId(id="1")
    planning_date = date(2023, 10, 10)
    create_planning(repo, planning_id, promotion_id, planning_date, [])

    results = repo.find_by_date_and_promotion(planning_date, promotion_id)
    assert len(results) == 1
    assert results[0].id == planning_id


def test_database_with_multiple_plannings_when_find_all_then_return_all_domain_plannings(session):
    repo = PlanningRepository(session)

    planning_1 = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[])
    planning_2 = Planning(id="2", date=date(2022, 1, 2), promotion_id="2", slots=[])

    session.add(planning_1)
    session.add(planning_2)
    session.commit()

    results = repo.find_all()

    assert len(results) == 2
    ids = {str(p.id) for p in results}
    assert ids == {"1", "2"}


def test_existing_planning_when_update_called_then_updates_are_applied(session):
    repo = PlanningRepository(session)
    db_planning = Planning(id="1", date=date(2022, 1, 1), promotion_id="1", slots=[])
    session.add(db_planning)
    session.commit()

    updated = DomainPlanning(id=PlanningId(id="1"), date=date(2022, 2, 2), promotion_id=PromotionId(id="2"), slots=[])
    repo.update(updated)

    refreshed = session.get(Planning, "1")
    assert refreshed.date == date(2022, 2, 2)
    assert refreshed.promotion_id == "2"


def test_nonexistent_planning_when_update_called_then_raise_value_error(session):
    repo = PlanningRepository(session)

    updated = DomainPlanning(id=PlanningId(id="999"), date=date(2022, 2, 2), promotion_id=PromotionId(id="2"), slots=[])

    with pytest.raises(ValueError, match="Planning not found"):
        repo.update(updated)


def test_existing_planning_with_slot_when_find_slot_by_id_then_return_domain_slot(session):
    repo = PlanningRepository(session)

    slot = PlanningSlot(
        id="slot-123", hours_start=9, minutes_start=0, hours_end=10, minutes_end=30,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="plan-123"
    )
    db_planning = Planning(id="plan-123", date=date(2022, 1, 1), promotion_id="1", slots=[slot])
    session.add(db_planning)
    session.commit()

    result = repo.find_slot_by_id(PlanningId(id="plan-123"), PlanningSlotId(id="slot-123"))
    assert result.id.id == "slot-123"
    assert result.hours_start == 9
    assert result.hours_end == 10


def test_nonexistent_slot_when_find_slot_by_id_then_raise_value_error(session):
    repo = PlanningRepository(session)

    with pytest.raises(ValueError, match="Planning slot not found"):
        repo.find_slot_by_id(PlanningId(id="nonexistent"), PlanningSlotId(id="missing"))


def test_existing_planning_when_add_slot_then_slot_is_persisted(session):
    repo = PlanningRepository(session)

    # Create planning without slots
    db_planning = Planning(id="plan-321", date=date(2022, 1, 1), promotion_id="1", slots=[])
    session.add(db_planning)
    session.commit()

    # Create slot and add it
    domain_slot = create_domain_slot(slot_id="slot-321")
    repo.add_slot(PlanningId(id="plan-321"), domain_slot)

    # Fetch and validate
    updated = session.get(Planning, "plan-321")
    assert len(updated.slots) == 1
    assert updated.slots[0].id == "slot-321"
    assert updated.slots[0].planning_id == "plan-321"


def test_existing_planning_when_update_slot_then_slot_is_updated(session):
    repo = PlanningRepository(session)

    # Create initial planning and slot
    db_slot = PlanningSlot(
        id="slot-456", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="plan-456"
    )
    db_planning = Planning(id="plan-456", date=date(2022, 1, 1), promotion_id="1", slots=[db_slot])
    session.add(db_planning)
    session.commit()

    # Update slot data via domain model
    updated_slot = DomainPlanningSlot(
        id=PlanningSlotId(id="slot-456"), hours_start=10, minutes_start=15, hours_end=12, minutes_end=45,
        promotion_id=PromotionId(id="1"), teacher_id=TeacherId(id="1"), course_id=CourseId(id="1"), room_id=RoomId(id="1")
    )
    repo.update_slot(PlanningId(id="plan-456"), updated_slot)

    # Validate
    refreshed_slot = session.get(PlanningSlot, "slot-456")
    assert refreshed_slot.hours_start == 10
    assert refreshed_slot.minutes_start == 15
    assert refreshed_slot.hours_end == 12
    assert refreshed_slot.minutes_end == 45


def test_wrong_planning_when_update_slot_then_raise_value_error(session):
    repo = PlanningRepository(session)

    # Create planning and slot with mismatched planning_id
    db_slot = PlanningSlot(
        id="slot-789", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="correct-plan"
    )
    session.add(db_slot)
    session.commit()

    # Try updating with wrong planning_id
    updated_slot = DomainPlanningSlot(
        id=PlanningSlotId(id="slot-789"), hours_start=10, minutes_start=0, hours_end=11, minutes_end=0,
        promotion_id=PromotionId(id="1"), teacher_id=TeacherId(id="1"), course_id=CourseId(id="1"), room_id=RoomId(id="1")
    )

    with pytest.raises(ValueError, match="Planning slot not found"):
        repo.update_slot(PlanningId(id="wrong-plan"), updated_slot)


def test_existing_planning_when_delete_slot_then_slot_is_removed(session):
    repo = PlanningRepository(session)

    db_slot = PlanningSlot(
        id="slot-del", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="plan-del"
    )
    db_planning = Planning(id="plan-del", date=date(2022, 1, 1), promotion_id="1", slots=[db_slot])
    session.add(db_planning)
    session.commit()

    repo.delete_slot(PlanningId(id="plan-del"), PlanningSlotId(id="slot-del"))

    assert session.get(PlanningSlot, "slot-del") is None


def test_wrong_planning_when_delete_slot_then_raise_value_error(session):
    repo = PlanningRepository(session)

    db_slot = PlanningSlot(
        id="slot-wrong", hours_start=9, minutes_start=0, hours_end=10, minutes_end=0,
        promotion_id="1", teacher_id="1", course_id="1", room_id="1", planning_id="correct-plan"
    )
    session.add(db_slot)
    session.commit()

    with pytest.raises(ValueError, match="Planning slot not found"):
        repo.delete_slot(PlanningId(id="wrong-plan"), PlanningSlotId(id="slot-wrong"))
