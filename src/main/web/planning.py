from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import date as dt
from src.main import domain
from src.main.web.auth import get_current_user
from src.main.web import state
from src.main.web.promotions import Promotion
from src.main.web.teachers import Teacher
from src.main.web.courses import Course
from src.main.web.rooms import Room
from pydantic import BaseModel
import uuid

router = APIRouter(tags=["Planning"])

class PlanningSlot(BaseModel):
    id: str
    hours_start: int
    minutes_start: int
    hours_end: int
    minutes_end: int
    promotion: Promotion
    teacher: Teacher
    course: Course
    room: Room

class PlanningSlotWrite(BaseModel):
    id: str
    hours_start: int
    minutes_start: int
    hours_end: int
    minutes_end: int
    promotion_id: str
    teacher_id: str
    course_id: str
    room_id: str

class Planning(BaseModel):
    id: str
    date: dt
    promotion: Promotion
    slots: List[Optional[PlanningSlot]]

class PlanningWrite(BaseModel):
    id: str
    date: dt
    promotion_id: str
    slots: List[Optional[PlanningSlotWrite]]

async def get_entity_by_id(repository, entity_id, entity_name):
    entity = repository.find_by_id(entity_id)
    if not entity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{entity_name} not found")
    return entity

async def get_planning_slot_from_entity(entity: domain.PlanningSlot) -> PlanningSlot:
    promotion = await get_promotion_from_entity(await get_entity_by_id(state.repository_promotions, entity.promotion_id, "Promotion"))
    teacher = await get_teacher_from_entity(await get_entity_by_id(state.repository_teachers, entity.teacher_id, "Teacher"))
    course = await get_course_from_entity(await get_entity_by_id(state.repository_courses, entity.course_id, "Course"))
    room = await get_room_from_entity(await get_entity_by_id(state.repository_rooms, entity.room_id, "Room"))
    return PlanningSlot(
        id=str(entity.id),
        hours_start=entity.hours_start,
        minutes_start=entity.minutes_start,
        hours_end=entity.hours_end,
        minutes_end=entity.minutes_end,
        promotion=promotion,
        teacher=teacher,
        course=course,
        room=room
    )

async def get_planning_from_entity(entity: domain.Planning) -> Planning:
    promotion = await get_promotion_from_entity(await get_entity_by_id(state.repository_promotions, str(entity.promotion_id), "Promotion"))
    slots = [await get_planning_slot_from_entity(slot) for slot in entity.slots]
    return Planning(id=str(entity.id), date=str(entity.date), promotion=promotion, slots=slots)

async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id), study_year=entity.study_year, diploma=entity.diploma, name=entity.name)

async def get_teacher_from_entity(entity: domain.Teacher) -> Teacher:
    return Teacher(id=str(entity.id), name=entity.name, firstname=entity.firstname)

async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)

async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)

async def validate_slot_details(slot: PlanningSlot):
    teacher = await get_entity_by_id(state.repository_teachers, slot.teacher.id, "Teacher")
    course = await get_entity_by_id(state.repository_courses, slot.course.id, "Course")
    room = await get_entity_by_id(state.repository_rooms, slot.room.id, "Room")
    return teacher, course, room

async def validate_slot_write_details(slot: PlanningSlotWrite):
    teacher = await get_entity_by_id(state.repository_teachers, slot.teacher_id, "Teacher")
    course = await get_entity_by_id(state.repository_courses, slot.course_id, "Course")
    room = await get_entity_by_id(state.repository_rooms, slot.room_id, "Room")
    return teacher, course, room

@router.get("/api/v1/plannings", response_model=List[Planning])
async def get_plannings(date: Optional[str] = None, promotion_id: Optional[str] = None) -> List[Planning]:
    planning_entities = state.repository_plannings.find_all()
    plannings = [await get_planning_from_entity(entity) for entity in planning_entities]
    return plannings

@router.post("/api/v1/plannings", response_model=Planning)
async def add_planning(planning: PlanningWrite) -> Planning:
    try:
        promotion = await get_entity_by_id(state.repository_promotions, planning.promotion_id, "Promotion")
        planning_slots = []
        for slot in planning.slots:
            teacher, course, room = await validate_slot_details(slot)
            planning_slot = domain.PlanningSlot(
                id=slot.id,
                hours_start=slot.hours_start,
                minutes_start=slot.minutes_start,
                hours_end=slot.hours_end,
                minutes_end=slot.minutes_end,
                promotion_id=planning.promotion_id,
                teacher_id=slot.teacher_id,
                course_id=slot.course_id,
                room_id=slot.room_id
            )
            planning_slots.append(planning_slot)

        planning_entity = domain.Planning(
            id=domain.PlanningId(id=planning.id),
            date=planning.date,
            promotion_id=domain.PromotionId(id=planning.promotion_id),
            slots=planning_slots
        )
        state.repository_plannings.save(planning_entity)
        return await get_planning_from_entity(planning_entity)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))

@router.get("/api/v1/plannings/{planning_id}", response_model=Planning)
async def get_planning_by_id(planning_id: str) -> Planning:
    try:
        planning = await get_entity_by_id(state.repository_plannings, planning_id, "Planning")
        return await get_planning_from_entity(planning)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))

@router.post("/api/v1/plannings/{planning_id}/slots", response_model=Planning)
async def add_planning_slot(planning_id: str, slot: PlanningSlotWrite) -> Planning:
    try:
        planning = await get_entity_by_id(state.repository_plannings, domain.PlanningId(id=planning_id), "Planning")
        teacher, course, room = await validate_slot_write_details(slot)

        planning_slot = domain.PlanningSlot(
            id=domain.PlanningSlotId(id=slot.id),
            hours_start=slot.hours_start,
            minutes_start=slot.minutes_start,
            hours_end=slot.hours_end,
            minutes_end=slot.minutes_end,
            promotion_id=domain.PromotionId(id=slot.promotion_id),
            teacher_id=domain.TeacherId(id=slot.teacher_id),
            course_id=domain.CourseId(id=slot.course_id),
            room_id=domain.RoomId(id=slot.room_id)
        )

        planning.slots.append(planning_slot)
        state.repository_plannings.save(planning)
        return await get_planning_from_entity(planning)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
