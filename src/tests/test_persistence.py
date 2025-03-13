import uuid
from src.main import domain


class BaseRepository:
    """Base repository with common functionality."""
    def next_identity(self):
        return str(uuid.uuid4())


class PromotionRepositoryDumb(BaseRepository, domain.IPromotionRepository):
    """Dumb implementation of IPromotionRepository."""
    def __init__(self):
        self.promotions = [
            domain.Promotion(id=domain.PromotionId(id=self.next_identity()), study_year=2, diploma="DEUST", name="Kempf"),
            domain.Promotion(id=domain.PromotionId(id=self.next_identity()), study_year=5, diploma="M2", name="Maisonnier")
        ]

    def find_all(self):
        return self.promotions


class PromotionRepositoryException(PromotionRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")


class PlanningRepositoryDumb(BaseRepository, domain.IPlanningRepository):
    """Dumb implementation of IPlanningRepository."""
    def __init__(self):
        self.plannings = [
            domain.Planning(
                id=domain.PlanningId(id=self.next_identity()),
                slots=self._create_slots()
            )
        ]

    def _create_slots(self):
        return [
            domain.PlanningSlot(
                id=domain.PlanningSlotId(id=self.next_identity()),
                date_start="2021-09-01",
                hours_start=9,
                minutes_start=0,
                hours_end=10,
                minutes_end=0,
                promotion=domain.Promotion(
                    id=domain.PromotionId(id=self.next_identity()), study_year=2, diploma="DEUST", name="Kempf"),
                teacher=domain.Teacher(id=domain.TeacherId(id=self.next_identity()), name="Doe", firstname="John"),
                course=domain.Course(id=domain.CourseId(id=self.next_identity()), name="Mathematics"),
                room=domain.Room(id=domain.RoomId(id=self.next_identity()), name="Room 101", description="First floor room")
            ),
            domain.PlanningSlot(
                id=domain.PlanningSlotId(id=self.next_identity()),
                date_start="2021-09-01",
                hours_start=10,
                minutes_start=15,
                hours_end=11,
                minutes_end=15,
                promotion=domain.Promotion(
                    id=domain.PromotionId(id=self.next_identity()), study_year=3, diploma="DEUST", name="Smith"),
                teacher=domain.Teacher(id=domain.TeacherId(id=self.next_identity()), name="Brown", firstname="Alice"),
                course=domain.Course(id=domain.CourseId(id=self.next_identity()), name="Physics"),
                room=domain.Room(id=domain.RoomId(id=self.next_identity()), name="Room 102", description="Second floor room")
            )
        ]

    def find_all(self):
        return self.plannings
