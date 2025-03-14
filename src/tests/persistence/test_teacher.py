from src.main.domain import BaseRepository, ITeacherRepository, Teacher, TeacherId

class TeacherRepositoryDumb(BaseRepository, ITeacherRepository):
    """Dumb implementation of ITeacherRepository."""
    def __init__(self):
        self.teachers = [
            Teacher(id=TeacherId(id="1"), name="Doe", firstname="John"),
            Teacher(id=TeacherId(id="2"), name="Smith", firstname="Jane")
        ]

    def find_all(self):
        return self.teachers

    def find_by_id(self, id: TeacherId):
        for teacher in self.teachers:
            if teacher.id == id:
                return teacher
        raise ValueError("Teacher not found")

class TeacherRepositoryException(TeacherRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: TeacherId):
        raise Exception("Test exception")
