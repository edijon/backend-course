from src.main.domain import Course as DomainCourse
from src.main.domain import BaseRepository, ICourseRepository, CourseId
from sqlmodel import Session, create_engine, SQLModel
from src.main.persistence.course import Course, CourseRepository
import pytest


class CourseRepositoryDumb(BaseRepository, ICourseRepository):
    """Dumb implementation of ICourseRepository."""
    def __init__(self):
        self.courses = [
            DomainCourse(id=CourseId(id="1"), name="Course A"),
            DomainCourse(id=CourseId(id="2"), name="Course B")
        ]

    def find_all(self):
        return self.courses

    def find_by_id(self, id: CourseId):
        for course in self.courses:
            if str(course.id) == str(id):
                return course
        raise ValueError("Course not found")

class CourseRepositoryException(CourseRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: CourseId):
        raise Exception("Test exception")


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_course_repository(session):
    # Given
    name = "Course A"
    repository = CourseRepository(session)
    course_id = repository.next_identity()
    course = DomainCourse(id=course_id, name=name)
    
    # When
    repository.add(course)
    assert course.id is not None

    fetched_course = repository.find_by_id(course.id)
    assert fetched_course is not None
    assert fetched_course.name == "Course A"

    fetched_course.name = "Course B"
    repository.update(fetched_course)
    updated_course = repository.find_by_id(fetched_course.id)
    assert updated_course.name == "Course B"

    repository.delete(updated_course.id)
    with pytest.raises(ValueError):
        repository.find_by_id(updated_course.id)
