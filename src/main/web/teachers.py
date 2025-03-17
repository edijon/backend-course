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
    """
    try:
        teacher_entity = domain.Teacher(
            id=domain.TeacherId(id=teacher.id),
            name=teacher.name,
            firstname=teacher.firstname
        )
        state.repository_teachers.add(teacher_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return teacher


@router.put("/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: str, teacher: Teacher, user: dict = Depends(get_current_user)) -> Teacher:
    """
    Update an existing teacher's information.
    """
    try:
        teacher_entity = state.repository_teachers.find_by_id(domain.TeacherId(id=teacher_id))
        teacher_entity.name = teacher.name
        teacher_entity.firstname = teacher.firstname
        state.repository_teachers.update(teacher_entity)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return teacher


@router.delete("/{teacher_id}", response_model=dict)
async def delete_teacher(teacher_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a teacher by their ID.
    """
    try:
        teacher_entity = state.repository_teachers.find_by_id(domain.TeacherId(id=teacher_id))
        if not teacher_entity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
        state.repository_teachers.delete(domain.TeacherId(id=teacher_id))
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return {"message": "Teacher deleted"}


async def get_teacher_from_entity(entity: domain.Teacher) -> Teacher:
    return Teacher(id=str(entity.id), name=entity.name, firstname=entity.firstname)
