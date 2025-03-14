from src.main.domain.teacher import Teacher, TeacherId
import pytest

class TestTeacher:
    """Test cases for Teacher class."""
    
    def test_given_name_and_firstname_when_create_teacher_then_return_teacher(self):
        # Given
        teacher_id = TeacherId(id="1")
        name = "Doe"
        firstname = "John"
        # When
        teacher = Teacher(id=teacher_id, name=name, firstname=firstname)
        # Then
        assert teacher.name == name
        assert teacher.firstname == firstname
