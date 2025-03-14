from src.main.domain import Teacher as DomainTeacher
from src.main.domain import BaseRepository, ITeacherRepository, TeacherId
from sqlmodel import Session, create_engine, SQLModel
from src.main.persistence.teacher import Teacher, TeacherRepository
import pytest

class TeacherRepositoryDumb(BaseRepository, ITeacherRepository):
    """Dumb implementation of ITeacherRepository."""
    def __init__(self):
        self.teachers = [
            DomainTeacher(id=TeacherId(id="1"), name="Doe", firstname="John"),
            DomainTeacher(id=TeacherId(id="2"), name="Smith", firstname="Jane")
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


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_teacher_repository(session):
    # Given
    name = "Doe"
    firstname = "John"
    repository = TeacherRepository(session)
    teacher_id = repository.next_identity()
    teacher = DomainTeacher(id=teacher_id, name=name, firstname=firstname)
    
    # When
    repository.add(teacher)
    assert teacher.id is not None

    fetched_teacher = repository.find_by_id(teacher.id)
    assert fetched_teacher is not None
    assert fetched_teacher.name == "Doe"
    assert fetched_teacher.firstname == "John"

    fetched_teacher.name = "Smith"
    repository.update(fetched_teacher)
    updated_teacher = repository.find_by_id(fetched_teacher.id)
    assert updated_teacher.name == "Smith"

    repository.delete(updated_teacher.id)
    with pytest.raises(ValueError):
        repository.find_by_id(updated_teacher.id)
