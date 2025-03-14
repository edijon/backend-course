from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from .base import BaseIdentifier

class TeacherId(BaseIdentifier):
    """Value object holding Teacher identity."""
    pass

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

    @abstractmethod
    def find_by_id(self, id: TeacherId) -> Teacher:
        raise NotImplementedError
