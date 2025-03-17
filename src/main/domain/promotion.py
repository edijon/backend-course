from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from .base import BaseIdentifier


class PromotionId(BaseIdentifier):
    """Value object holding Promotion identity."""
    pass


class Promotion(BaseModel):
    """Aggregate root, entity holding promotion."""
    id: PromotionId
    study_year: int
    diploma: str
    name: str


class IPromotionRepository(ABC):
    """Interface for handling promotions persistence."""
    @abstractmethod
    def next_identity(self) -> PromotionId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Promotion]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: PromotionId) -> Promotion:
        raise NotImplementedError

    @abstractmethod
    def add(self, promotion: Promotion) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, promotion: Promotion) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: PromotionId) -> None:
        raise NotImplementedError
