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
