from sqlmodel import Session, select, SQLModel, Field
from typing import List
from src.main.domain.course import ICourseRepository, Course as DomainCourse, CourseId
from src.main.domain.base import BaseRepository


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    name: str


class CourseRepository(BaseRepository, ICourseRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[DomainCourse]:
        statement = select(Course)
        results = self.session.exec(statement)
        return [self._to_domain(course) for course in results.all()]

    def find_by_id(self, id: CourseId) -> DomainCourse:
        statement = select(Course).where(Course.id == str(id))
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Course not found")
        return self._to_domain(result)

    def add(self, course: DomainCourse) -> None:
        db_course = Course(
            id=str(course.id),
            name=course.name
        )
        self.session.add(db_course)
        self.session.commit()

    def update(self, course: DomainCourse) -> None:
        db_course = Course(
            id=str(course.id),
            name=course.name
        )
        self.session.merge(db_course)
        self.session.commit()

    def delete(self, id: CourseId) -> None:
        db_course = self.session.get(Course, str(id))
        self.session.delete(db_course)
        self.session.commit()

    def _to_domain(self, course: Course) -> DomainCourse:
        return DomainCourse(
            id=CourseId(id=course.id),
            name=course.name
        )
