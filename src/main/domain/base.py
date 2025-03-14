from pydantic import BaseModel, ConfigDict


class BaseIdentifier(BaseModel):
    """Value object holding Component identity."""
    id: str
    model_config = ConfigDict(frozen=True)

    def __str__(self):
        return self.id


class BaseRepository:
    """Base repository with common functionality."""
    def next_identity(self):
        import uuid
        return str(uuid.uuid4())
