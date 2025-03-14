from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.main import domain
from src.main.web.auth import get_current_user
from src.main.web import state
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/courses", tags=["Courses"])

class Course(BaseModel):
    id: str
    name: str

@router.get("", response_model=List[Course])
async def get_courses() -> List[Course]:
    """
    Fetches a list of courses.
    This asynchronous function retrieves all course entities from the repository,
    converts them to course objects, and returns them as a list.
    Returns:
        List[Course]: A list of course objects.
    HTTP Status Codes:
        200 OK: Successfully retrieved the list of courses.
        500 Internal Server Error: An error occurred while fetching the courses.
    """
    try:
        course_entities = state.repository_courses.find_all()
        courses = [await get_course_from_entity(entity) for entity in course_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return courses

@router.post("", response_model=Course)
async def add_course(course: Course, user: dict = Depends(get_current_user)) -> Course:
    """
    Add a new course to the repository.
    Args:
        course (Course): The course object to be added.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from `get_current_user`.
    Returns:
        Course: The added course object.
    HTTP Status Codes:
        201 Created: If the course is successfully added.
        401 Unauthorized: If the user is not authenticated.
        403 Forbidden: If the user does not have permission to add a course.
        500 Internal Server Error: If there is an error while adding the course.
    """
    # Add logic to save the course to the repository
    return course

@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: str, course: Course, user: dict = Depends(get_current_user)) -> Course:
    """
    Update an existing course.
    Args:
        course_id (str): The unique identifier of the course to be updated.
        course (Course): The course object containing updated information.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from `get_current_user`.
    Returns:
        Course: The updated course object.
    HTTP Status Codes:
        200 OK: The course was successfully updated.
        400 Bad Request: The request was invalid or cannot be otherwise served.
        401 Unauthorized: Authentication credentials were missing or incorrect.
        404 Not Found: The course with the specified ID was not found.
        500 Internal Server Error: An error occurred on the server.
    """
    # Add logic to update the course in the repository
    return course

@router.delete("/{course_id}", response_model=dict)
async def delete_course(course_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a course by its ID.
    Args:
        course_id (str): The ID of the course to be deleted.
        user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
    Returns:
        dict: A message indicating the course has been deleted.
    HTTP Status Codes:
        200 OK: Course successfully deleted.
        401 Unauthorized: User is not authenticated.
        403 Forbidden: User does not have permission to delete the course.
        404 Not Found: Course with the specified ID does not exist.
    """
    # Add logic to delete the course from the repository
    return {"message": "Course deleted"}

async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)
