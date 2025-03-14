from src.main.domain import BaseRepository, IRoomRepository, Room, RoomId

class RoomRepositoryDumb(BaseRepository, IRoomRepository):
    """Dumb implementation of IRoomRepository."""
    def __init__(self):
        self.rooms = [
            Room(id=RoomId(id="1"), name="Room 101", description="First floor room"),
            Room(id=RoomId(id="2"), name="Room 102", description="Second floor room")
        ]

    def find_all(self):
        return self.rooms

    def find_by_id(self, id: RoomId):
        for room in self.rooms:
            if room.id == id:
                return room
        raise ValueError("Room not found")

class RoomRepositoryException(RoomRepositoryDumb):
    def find_all(self):
        raise Exception("Test exception")

    def find_by_id(self, id: RoomId):
        raise Exception("Test exception")
