"""
This module contains the implementation of the REST API for the courses
endpoint using FastAPI.
"""
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
    try:
        course_entity = domain.Course(id=domain.CourseId(id=course.id), name=course.name)
        state.repository_courses.add(course_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return course


@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: str, course: Course, user: dict = Depends(get_current_user)) -> Course:
    """
    Update an existing course.
    """
    try:
        course_entity = state.repository_courses.find_by_id(domain.CourseId(id=course_id))
        if not course_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        course_entity.name = course.name
        state.repository_courses.update(course_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return course


@router.delete("/{course_id}", response_model=dict)
async def delete_course(course_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a course by its ID.
    """
    try:
        course_entity = state.repository_courses.find_by_id(domain.CourseId(id=course_id))
        if not course_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        state.repository_courses.delete(course_entity.id)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return {"message": "Course deleted"}


async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)
