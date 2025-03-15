from sqlmodel import Session, select, SQLModel, Field
from typing import List
from src.main.domain.room import IRoomRepository, Room as DomainRoom, RoomId
from src.main.domain.base import BaseRepository


class Room(SQLModel, table=True):
    __tablename__ = "rooms"
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    name: str
    description: str


class RoomRepository(BaseRepository, IRoomRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> List[DomainRoom]:
        statement = select(Room)
        results = self.session.exec(statement)
        return [self._to_domain(room) for room in results.all()]

    def find_by_id(self, id: RoomId) -> DomainRoom:
        statement = select(Room).where(Room.id == str(id))
        result = self.session.exec(statement).first()
        if not result:
            raise ValueError("Room not found")
        return self._to_domain(result)

    def add(self, room: DomainRoom) -> None:
        db_room = Room(
            id=str(room.id),
            name=room.name,
            description=room.description
        )
        self.session.add(db_room)
        self.session.commit()

    def update(self, room: DomainRoom) -> None:
        db_room = Room(
            id=str(room.id),
            name=room.name,
            description=room.description
        )
        self.session.merge(db_room)
        self.session.commit()

    def delete(self, id: RoomId) -> None:
        db_room = self.session.get(Room, str(id))
        self.session.delete(db_room)
        self.session.commit()

    def _to_domain(self, room: Room) -> DomainRoom:
        return DomainRoom(
            id=RoomId(id=room.id),
            name=room.name,
            description=room.description
        )
