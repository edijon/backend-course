from src.main.domain import BaseRepository, IPromotionRepository, Promotion, PromotionId

class PromotionRepositoryDumb(BaseRepository, IPromotionRepository):
    """Dumb implementation of IPromotionRepository."""
    def __init__(self):
        self.promotions = [
            Promotion(id=PromotionId(id="1"), study_year=2, diploma="DEUST", name="Kempf"),
            Promotion(id=PromotionId(id="2"), study_year=5, diploma="M2", name="Maisonnier")
        ]

    def find_all(self):
        return self.promotions

    def find_by_id(self, id: PromotionId):
        for promotion in self.promotions:
            if promotion.id == id:
                return promotion
        raise ValueError("Promotion not found")

class PromotionRepositoryException(PromotionRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: PromotionId):
        raise Exception("Test exception")
