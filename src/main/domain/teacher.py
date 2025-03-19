"""
This module contains the definition of the Teacher domain entity.
"""
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

    @abstractmethod
    def add(self, teacher: Teacher) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, teacher: Teacher) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: TeacherId) -> None:
        raise NotImplementedError
