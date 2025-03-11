from abc import ABC, abstractmethod
from pydantic import BaseModel, ConfigDict
from typing import List


class BaseIdentifier(BaseModel):
    """Value object holding Component identity."""
    id: str
    model_config = ConfigDict(frozen=True)

    def __str__(self):
        return self.id


class PromotionId(BaseIdentifier):
    """Value object holding Promotion identity."""


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


class TeacherId(BaseIdentifier):
    """Value object holding Teacher identity."""


class Teacher(BaseModel):
    """Aggregate root, entity holding teacher."""
    id: TeacherId
    name: str
    firstname: str


class ITeacherRepository(ABC):
    """Interface for handling teachers persistence."""
    @abstractmethod
    def next_identity(self) -> TeacherId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Teacher]:
        raise NotImplementedError
