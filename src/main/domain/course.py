"""
This module contains the definition of the Course domain entity.
"""
from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from .base import BaseIdentifier


class CourseId(BaseIdentifier):
    """Value object holding Course identity."""
    pass


class Course(BaseModel):
    """Aggregate root, entity holding course."""
    id: CourseId
    name: str


class ICourseRepository(ABC):
    """Interface for handling courses persistence."""
    @abstractmethod
    def next_identity(self) -> CourseId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Course]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: CourseId) -> Course:
        raise NotImplementedError

    @abstractmethod
    def add(self, course: Course) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, course: Course) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: CourseId) -> None:
        raise NotImplementedError
