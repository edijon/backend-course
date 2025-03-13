import src.main.domain as domain
from datetime import date


class PromotionRepositoryDumb(domain.BaseRepository, domain.IPromotionRepository):
    """Dumb implementation of IPromotionRepository."""
    def __init__(self):
        self.promotions = [
            domain.Promotion(id=domain.PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf"),
            domain.Promotion(id=domain.PromotionId(id="2"), study_year=5, diploma="M2", name="Maisonnier")
        ]

    def find_all(self):
        return self.promotions

    def find_by_id(self, id: domain.PromotionId):
        for promotion in self.promotions:
            if promotion.id == id:
                return promotion
        raise ValueError("Promotion not found")


class PromotionRepositoryException(PromotionRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: domain.PromotionId):
        raise Exception("Test exception")


class TeacherRepositoryDumb(domain.BaseRepository, domain.ITeacherRepository):
    """Dumb implementation of ITeacherRepository."""
    def __init__(self):
        self.teachers = [
            domain.Teacher(id=domain.TeacherId(id="1"), name="Doe", firstname="John"),
            domain.Teacher(id=domain.TeacherId(id="2"), name="Smith", firstname="Jane")
        ]

    def find_all(self):
        return self.teachers

    def find_by_id(self, id: domain.TeacherId):
        for teacher in self.teachers:
            if teacher.id == id:
                return teacher
        raise ValueError("Teacher not found")


class CourseRepositoryDumb(domain.BaseRepository, domain.ICourseRepository):
    """Dumb implementation of ICourseRepository."""
    def __init__(self):
        self.courses = [
            domain.Course(id=domain.CourseId(id="1"), name="Mathematics"),
            domain.Course(id=domain.CourseId(id="2"), name="Physics")
        ]

    def find_all(self):
        return self.courses

    def find_by_id(self, id: domain.CourseId):
        for course in self.courses:
            if course.id == id:
                return course
        raise ValueError("Course not found")


class RoomRepositoryDumb(domain.BaseRepository, domain.IRoomRepository):
    """Dumb implementation of IRoomRepository."""
    def __init__(self):
        self.rooms = [
            domain.Room(id=domain.RoomId(id="1"), name="Room 101", description="First floor room"),
            domain.Room(id=domain.RoomId(id="2"), name="Room 102", description="Second floor room")
        ]

    def find_all(self):
        return self.rooms

    def find_by_id(self, id: domain.RoomId):
        for room in self.rooms:
            if room.id == id:
                return room
        raise ValueError("Room not found")


class PlanningRepositoryDumb(domain.BaseRepository, domain.IPlanningRepository):
    """Dumb implementation of IPlanningRepository."""
    def __init__(self):
        self.plannings = [
            domain.Planning(
                id=domain.PlanningId(id="1"),
                slots=self._create_slots()
            )
        ]

    def _create_slots(self):
        return [
            domain.PlanningSlot(
                id=domain.PlanningSlotId(id="1"),
                date_start=date(2021, 9, 1),
                hours_start=9,
                minutes_start=0,
                hours_end=10,
                minutes_end=0,
                promotion_id=domain.PromotionId(id="1"),
                teacher_id=domain.TeacherId(id="1"),
                course_id=domain.CourseId(id="1"),
                room_id=domain.RoomId(id="1")
            ),
            domain.PlanningSlot(
                id=domain.PlanningSlotId(id="2"),
                date_start=date(2021, 9, 1),
                hours_start=10,
                minutes_start=15,
                hours_end=11,
                minutes_end=15,
                promotion_id=domain.PromotionId(id="2"),
                teacher_id=domain.TeacherId(id="2"),
                course_id=domain.CourseId(id="2"),
                room_id=domain.RoomId(id="2")
            )
        ]

    def find_all(self):
        return self.plannings

    def find_by_id(self, id: domain.PlanningId):
        for planning in self.plannings:
            if planning.id == id:
                return planning
        raise ValueError("Planning not found")
