from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
from src.main import domain


repository = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Defines both startup (before yield) and shutdown events."""
    global repository
    repository = None
    yield


app = FastAPI(lifespan=lifespan)


class Promotion(BaseModel):
    id: str
    study_year: str = ""
    diploma: str = "FR"
    name: str = ""


class Teacher(BaseModel):
    id: str
    name: str
    firstname: str


class Course(BaseModel):
    id: str
    name: str


class Room(BaseModel):
    id: str
    name: str
    description: str


class PlanningSlot(BaseModel):
    id: str
    date_start: str
    hours_start: int
    minutes_start: int
    hours_end: int
    minutes_end: int
    promotion: Promotion
    teacher: Teacher
    course: Course
    room: Room


class Planning(BaseModel):
    id: str
    slots: List[PlanningSlot]


@app.get("/api/v1/promotions", response_model=List[Promotion])
async def get_promotions() -> List[Promotion]:
    """List all promotions."""
    global repository
    try:
        promotion_entities = repository.find_all()
        promotions = []
        for entity in promotion_entities:
            promotion = await get_promotion_from_entity(entity=entity)
            promotions.append(promotion)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return promotions


@app.get("/api/v1/planning", response_model=List[Planning])
async def get_planning() -> List[Planning]:
    """List all planning."""
    global repository
    try:
        planning_entities = repository.find_all()
        plannings = []
        for entity in planning_entities:
            planning = await get_planning_from_entity(entity=entity)
            plannings.append(planning)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return plannings


async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id))


async def get_planning_from_entity(entity: domain.Planning) -> Planning:
    slots = [await get_planning_slot_from_entity(slot) for slot in entity.slots]
    return Planning(id=str(entity.id), slots=slots)


async def get_planning_slot_from_entity(entity: domain.PlanningSlot) -> PlanningSlot:
    promotion = await get_promotion_from_entity(entity.promotion)
    teacher = Teacher(id=str(entity.teacher.id), name=entity.teacher.name, firstname=entity.teacher.firstname)
    course = Course(id=str(entity.course.id), name=entity.course.name)
    room = Room(id=str(entity.room.id), name=entity.room.name, description=entity.room.description)
    return PlanningSlot(
        id=str(entity.id),
        date_start=str(entity.date_start),
        hours_start=entity.hours_start,
        minutes_start=entity.minutes_start,
        hours_end=entity.hours_end,
        minutes_end=entity.minutes_end,
        promotion=promotion,
        teacher=teacher,
        course=course,
        room=room
    )
