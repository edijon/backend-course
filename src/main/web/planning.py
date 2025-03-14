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

router = APIRouter(tags=["Planning"])

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
    date: str
    promotion: Promotion
    slots: List[PlanningSlot]

@router.get("/api/v1/planning-slots", response_model=List[PlanningSlot])
async def get_planning_slots() -> List[PlanningSlot]:
    """
    Fetches all planning slots.
    This asynchronous function retrieves all planning slots from the repository and converts them into a list of PlanningSlot objects.
    Returns:
        List[PlanningSlot]: A list of planning slots.
    Raises:
        HTTPException: If an error occurs while fetching the planning slots, an HTTP 500 status code is returned.
    """
    try:
        planning_slot_entities = state.repository_plannings.find_all_slots()
        planning_slots = [await get_planning_slot_from_entity(entity) for entity in planning_slot_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return planning_slots

@router.post("/api/v1/planning-slots", response_model=PlanningSlot)
async def add_planning_slot(planning_slot: PlanningSlot, user: dict = Depends(get_current_user)) -> PlanningSlot:
    """
    Add a new planning slot.
    This endpoint allows the user to add a new planning slot to the repository.
    Args:
        planning_slot (PlanningSlot): The planning slot to be added.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from the dependency injection.
    Returns:
        PlanningSlot: The planning slot that was added.
    HTTP Status Codes:
        200 OK: The planning slot was successfully added.
        401 Unauthorized: The user is not authenticated.
        403 Forbidden: The user does not have permission to add a planning slot.
        500 Internal Server Error: An error occurred while adding the planning slot.
    """
    # Add logic to save the planning slot to the repository
    return planning_slot

@router.put("/api/v1/planning-slots/{planning_slot_id}", response_model=PlanningSlot)
async def update_planning_slot(planning_slot_id: str, planning_slot: PlanningSlot, user: dict = Depends(get_current_user)) -> PlanningSlot:
    """
    Update a planning slot.
    This endpoint allows the user to update an existing planning slot with new information.
    Args:
        planning_slot_id (str): The unique identifier of the planning slot to be updated.
        planning_slot (PlanningSlot): The new planning slot data to replace the existing one.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from the `get_current_user` dependency.
    Returns:
        PlanningSlot: The updated planning slot.
    HTTP Status Codes:
        200 OK: The planning slot was successfully updated.
        400 Bad Request: The provided data is invalid.
        401 Unauthorized: The user is not authenticated.
        403 Forbidden: The user does not have permission to update the planning slot.
        404 Not Found: The planning slot with the given ID does not exist.
    """
    # Add logic to update the planning slot in the repository
    return planning_slot

@router.delete("/api/v1/planning-slots/{planning_slot_id}", response_model=dict)
async def delete_planning_slot(planning_slot_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a planning slot.
    This endpoint deletes a planning slot identified by the given planning_slot_id.
    Args:
        planning_slot_id (str): The unique identifier of the planning slot to be deleted.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from the get_current_user dependency.
    Returns:
        dict: A message indicating the result of the deletion operation.
    HTTP Status Codes:
        200 OK: Planning slot successfully deleted.
        401 Unauthorized: If the user is not authenticated.
        403 Forbidden: If the user does not have permission to delete the planning slot.
        404 Not Found: If the planning slot does not exist.
    """
    # Add logic to delete the planning slot from the repository
    return {"message": "Planning slot deleted"}

@router.get("/api/v1/planning", response_model=List[Planning])
async def get_planning(date: Optional[str] = None, promotion_id: Optional[str] = None) -> List[Planning]:
    """
    Fetches planning information based on the provided date and promotion ID.
    Args:
        date (str, optional): The date for which to fetch planning information in ISO format (YYYY-MM-DD). Defaults to None.
        promotion_id (str, optional): The ID of the promotion for which to fetch planning information. Defaults to None.
    Returns:
        List[Planning]: A list of Planning objects that match the provided criteria.
    HTTP Status Codes:
        200 OK: Returned when the planning information is successfully retrieved.
        500 Internal Server Error: Returned when there is an error processing the request.
    """
    try:
        if date and promotion_id:
            planning_entities = state.repository_plannings.find_by_date_and_promotion(
                dt.fromisoformat(date),
                domain.PromotionId(id=promotion_id)
            )
        else:
            planning_entities = state.repository_plannings.find_all()
        plannings = [await get_planning_from_entity(entity) for entity in planning_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return plannings

async def get_planning_slot_from_entity(entity: domain.PlanningSlot) -> PlanningSlot:
    promotion = await get_promotion_from_entity(state.repository_promotions.find_by_id(entity.promotion_id))
    teacher = await get_teacher_from_entity(state.repository_teachers.find_by_id(entity.teacher_id))
    course = await get_course_from_entity(state.repository_courses.find_by_id(entity.course_id))
    room = await get_room_from_entity(state.repository_rooms.find_by_id(entity.room_id))
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

async def get_planning_from_entity(entity: domain.Planning) -> Planning:
    promotion = await get_promotion_from_entity(state.repository_promotions.find_by_id(entity.promotion_id))
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
