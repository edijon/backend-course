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
    """
    # Add logic to save the course to the repository
    return course


@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: str, course: Course, user: dict = Depends(get_current_user)) -> Course:
    """
    Update an existing course.
    """
    # Add logic to update the course in the repository
    return course


@router.delete("/{course_id}", response_model=dict)
async def delete_course(course_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a course by its ID.
    """
    # Add logic to delete the course from the repository
    return {"message": "Course deleted"}


async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)
