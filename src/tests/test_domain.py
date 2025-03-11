from src.main.domain import Promotion, PromotionId, Teacher, TeacherId


class TestPromotion:
    """Test cases for Promotion class."""
    def test_given_study_year_and_diploma_and_name_when_create_promotion_then_return_promotion(self):
        # Given
        promotion_id = PromotionId(id="1")
        study_year = 2
        diploma = "DEUST"
        name = "Kempf"
        # When
        promotion = Promotion(id=promotion_id, study_year=study_year, diploma=diploma, name=name)
        # Then
        assert promotion.study_year == study_year
        assert promotion.diploma == diploma
        assert promotion.name == name


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
