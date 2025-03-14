from src.main.domain.course import Course, CourseId
import pytest

class TestCourse:
    """Test cases for Course class."""
    
    def test_given_name_when_create_course_then_return_course(self):
        # Given
        course_id = CourseId(id="1")
        name = "Mathematics"
        # When
        course = Course(id=course_id, name=name)
        # Then
        assert course.name == name
