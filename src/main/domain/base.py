"""
This module contains basic classes from which all domain objects will inherit.
"""
from pydantic import BaseModel, ConfigDict
import uuid


class BaseIdentifier(BaseModel):
    """Value object holding Component identity."""
    id: str
    model_config = ConfigDict(frozen=True)

    def __str__(self):
        return self.id


class BaseRepository:
    """Base repository with common functionality."""
    def next_identity(self):
        return str(uuid.uuid4())
