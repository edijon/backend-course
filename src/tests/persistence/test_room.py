from src.main.domain import Room as DomainRoom
from src.main.domain import BaseRepository, IRoomRepository, RoomId
from sqlmodel import Session, create_engine, SQLModel
from src.main.persistence.room import Room, RoomRepository
import pytest


class RoomRepositoryDumb(BaseRepository, IRoomRepository):
    """Dumb implementation of IRoomRepository."""
    def __init__(self):
        self.rooms = [
            DomainRoom(id=RoomId(id="1"), name="Room A", description="Description A"),
            DomainRoom(id=RoomId(id="2"), name="Room B", description="Description B")
        ]

    def find_all(self):
        return self.rooms

    def find_by_id(self, id: RoomId):
        for room in self.rooms:
            if str(room.id) == str(id):
                return room
        raise ValueError("Room not found")

class RoomRepositoryException(RoomRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: RoomId):
        raise Exception("Test exception")


DATABASE_URL = "sqlite:///test.db"
engine = create_engine(DATABASE_URL)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

def test_room_repository(session):
    # Given
    name = "Room A"
    description = "Description A"
    repository = RoomRepository(session)
    room_id = repository.next_identity()
    room = DomainRoom(id=room_id, name=name, description=description)
    
    # When
    repository.add(room)
    assert room.id is not None

    fetched_room = repository.find_by_id(room.id)
    assert fetched_room is not None
    assert fetched_room.name == "Room A"
    assert fetched_room.description == "Description A"

    fetched_room.name = "Room B"
    repository.update(fetched_room)
    updated_room = repository.find_by_id(fetched_room.id)
    assert updated_room.name == "Room B"

    repository.delete(updated_room.id)
    with pytest.raises(ValueError):
        repository.find_by_id(updated_room.id)
