from src.main.domain.promotion import Promotion, PromotionId


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
