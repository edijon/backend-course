from src.main.domain import BaseRepository, ICourseRepository, Course, CourseId

class CourseRepositoryDumb(BaseRepository, ICourseRepository):
    """Dumb implementation of ICourseRepository."""
    def __init__(self):
        self.courses = [
            Course(id=CourseId(id="1"), name="Mathematics"),
            Course(id=CourseId(id="2"), name="Physics")
        ]

    def find_all(self):
        return self.courses

    def find_by_id(self, id: CourseId):
        for course in self.courses:
            if course.id == id:
                return course
        raise ValueError("Course not found")

class CourseRepositoryException(CourseRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: CourseId):
        raise Exception("Test exception")
