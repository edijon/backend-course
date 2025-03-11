import uuid
from src.main import domain


class PromotionRepositoryDumb(domain.IPromotionRepository):
    """Dumb implementation of IPromotionRepository."""
    def __init__(self):
        self.promotions = [
            domain.Promotion(id=domain.PromotionId(id=self.next_identity()), study_year=2, diploma="DEUST", name="Kempf"),
            domain.Promotion(id=domain.PromotionId(id=self.next_identity()), study_year=5, diploma="M2", name="Maisonnier")]

    def next_identity(self):
        return str(uuid.uuid4())

    def find_all(self):
        return self.promotions


class PromotionRepositoryException(PromotionRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")
