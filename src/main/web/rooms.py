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
    Returns:
        List[Room]: A list of Room objects.
    HTTP Status Codes:
        200 OK: Successfully retrieved the list of rooms.
        500 Internal Server Error: An error occurred while fetching the rooms.
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
    Args:
        room (Room): The room object to be added.
        user (dict, optional): The current user making the request, 
                               automatically injected by Depends(get_current_user).
    Returns:
        Room: The added room object.
    HTTP Status Codes:
        200 OK: Room successfully added.
        401 Unauthorized: If the user is not authenticated.
        403 Forbidden: If the user does not have permission to add a room.
        500 Internal Server Error: If there is an error saving the room.
    """
    # Add logic to save the room to the repository
    return room

@router.put("/{room_id}", response_model=Room)
async def update_room(room_id: str, room: Room, user: dict = Depends(get_current_user)) -> Room:
    """
    Update an existing room.
    Args:
        room_id (str): The unique identifier of the room to be updated.
        room (Room): The room object containing updated information.
        user (dict, optional): The current authenticated user. Defaults to the result of Depends(get_current_user).
    Returns:
        Room: The updated room object.
    HTTP Status Codes:
        200 OK: Room updated successfully.
        400 Bad Request: Invalid room data provided.
        401 Unauthorized: Authentication credentials were missing or incorrect.
        404 Not Found: Room with the specified ID does not exist.
        500 Internal Server Error: An error occurred while updating the room.
    """
    # Add logic to update the room in the repository
    return room

@router.delete("/{room_id}", response_model=dict)
async def delete_room(room_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a room by its ID.
    Args:
        room_id (str): The ID of the room to be deleted.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from the dependency injection.
    Returns:
        dict: A message indicating the room has been deleted.
    Status Codes:
        200: Room successfully deleted.
        401: Unauthorized access.
        404: Room not found.
    """
    # Add logic to delete the room from the repository
    return {"message": "Room deleted"}

async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)
