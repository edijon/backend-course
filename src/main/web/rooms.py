from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.main import domain
from src.main.web.auth import get_current_user
from src.main.web import state
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1/rooms", tags=["Rooms"])


class Room(BaseModel):
    id: str
    name: str
    description: str


@router.get("", response_model=List[Room])
async def get_rooms() -> List[Room]:
    """
    Fetches a list of rooms.
    This asynchronous function retrieves all room entities from the repository,
    converts them to Room objects, and returns them as a list.
    """
    try:
        room_entities = state.repository_rooms.find_all()
        rooms = [await get_room_from_entity(entity) for entity in room_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return rooms


@router.post("", response_model=Room)
async def add_room(room: Room, user: dict = Depends(get_current_user)) -> Room:
    """
    Add a new room to the repository.
    """
    try:
        room_entity = domain.Room(id=domain.RoomId(
            id=state.repository_rooms.next_identity()),
            name=room.name, description=room.description)
        state.repository_rooms.add(room_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return room


@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, room: Room, user: dict = Depends(get_current_user)) -> Room:
    """
    Update an existing room.
    """
    try:
        room_entity = state.repository_rooms.find_by_id(domain.RoomId(id=room_id))
        if not room_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        room_entity.name = room.name
        room_entity.description = room.description
        state.repository_rooms.update(room_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return room


@router.delete("/{room_id}", response_model=dict)
async def delete_room(room_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a room by its ID.
    """
    try:
        room_entity = state.repository_rooms.find_by_id(domain.RoomId(id=room_id))
        if not room_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
        state.repository_rooms.delete(domain.RoomId(id=room_id))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return {"message": "Room deleted"}


async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)
