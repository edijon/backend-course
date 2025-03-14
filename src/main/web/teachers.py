from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.main import domain
from src.main.web.auth import get_current_user
from src.main.web import state
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/teachers", tags=["Teachers"])

class Teacher(BaseModel):
    id: str
    name: str
    firstname: str

@router.get("", response_model=List[Teacher])
async def get_teachers() -> List[Teacher]:
    """
    Fetches a list of teachers.
    This asynchronous function retrieves all teacher entities from the repository,
    converts them to Teacher objects, and returns them as a list.
    Returns:
        List[Teacher]: A list of Teacher objects.
    Raises:
        HTTPException: If an internal server error occurs, an HTTP 500 status code is returned.
    """
    try:
        teacher_entities = state.repository_teachers.find_all()
        teachers = [await get_teacher_from_entity(entity) for entity in teacher_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return teachers

@router.post("", response_model=Teacher)
async def add_teacher(teacher: Teacher, user: dict = Depends(get_current_user)) -> Teacher:
    """
    Add a new teacher to the repository.
    Args:
        teacher (Teacher): The teacher object to be added.
        user (dict, optional): The current authenticated user, automatically provided by dependency injection.
    Returns:
        Teacher: The added teacher object.
    HTTP Status Codes:
        201 Created: If the teacher is successfully added.
        401 Unauthorized: If the user is not authenticated.
        403 Forbidden: If the user does not have permission to add a teacher.
        500 Internal Server Error: If there is an error while adding the teacher.
    """
    # Add logic to save the teacher to the repository
    return teacher

@router.put("/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: str, teacher: Teacher, user: dict = Depends(get_current_user)) -> Teacher:
    """
    Update an existing teacher's information.
    Args:
        teacher_id (str): The unique identifier of the teacher to be updated.
        teacher (Teacher): The updated teacher object containing new information.
        user (dict, optional): The current authenticated user, automatically injected by Depends.
    Returns:
        Teacher: The updated teacher object.
    HTTP Status Codes:
        200 OK: Successfully updated the teacher.
        400 Bad Request: Invalid input data.
        401 Unauthorized: Authentication credentials were missing or incorrect.
        404 Not Found: Teacher with the specified ID does not exist.
        500 Internal Server Error: An error occurred while updating the teacher.
    """
    # Add logic to update the teacher in the repository
    return teacher

@router.delete("/{teacher_id}", response_model=dict)
async def delete_teacher(teacher_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a teacher by their ID.
    Args:
        teacher_id (str): The ID of the teacher to be deleted.
        user (dict, optional): The current authenticated user. Defaults to the result of get_current_user.
    Returns:
        dict: A message indicating the result of the deletion.
    HTTP Status Codes:
        200 OK: Teacher successfully deleted.
        401 Unauthorized: If the user is not authenticated.
        403 Forbidden: If the user does not have permission to delete the teacher.
        404 Not Found: If the teacher with the given ID does not exist.
    """
    # Add logic to delete the teacher from the repository
    return {"message": "Teacher deleted"}

async def get_teacher_from_entity(entity: domain.Teacher) -> Teacher:
    return Teacher(id=str(entity.id), name=entity.name, firstname=entity.firstname)
