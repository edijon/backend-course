"""
This module defines the Room domain entity and related abstractions for managing room persistence.
It includes the RoomId value object for uniquely identifying rooms, the Room aggregate root entity
that describes the room's attributes, and the IRoomRepository interface for room persistence operations.
The repository interface outlines methods for generating new room identities, retrieving rooms,
and performing CRUD operations.
"""
from typing import List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from .base import BaseIdentifier


class RoomId(BaseIdentifier):
    """Value object holding Room identity."""
    pass


class Room(BaseModel):
    """Aggregate root, entity holding room."""
    id: RoomId
    name: str
    description: str


class IRoomRepository(ABC):
    """Interface for handling rooms persistence."""
    @abstractmethod
    def next_identity(self) -> RoomId:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: RoomId) -> Room:
        raise NotImplementedError

    @abstractmethod
    def add(self, room: Room) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, room: Room) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: RoomId) -> None:
        raise NotImplementedError
