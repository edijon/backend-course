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
    # Add logic to save the room to the repository
    return room


@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, room: Room, user: dict = Depends(get_current_user)) -> Room:
    """
    Update an existing room.
    """
    # Add logic to update the room in the repository
    return room


@router.delete("/{room_id}", response_model=dict)
async def delete_room(room_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a room by its ID.
    """
    # Add logic to delete the room from the repository
    return {"message": "Room deleted"}


async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)
