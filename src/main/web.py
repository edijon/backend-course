from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List
from datetime import date as dt
from src.main import domain


# Global repository variable
repository_promotions = None
repository_plannings = None
repository_teachers = None
repository_courses = None
repository_rooms = None


# OAuth2PasswordBearer is a class that provides a simple way to handle OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Fake function to decode tokens
# In a real application, you would use a proper library to decode and verify tokens
def fake_decode_token(token):
    if token == "fake-super-secret-token":
        return {"sub": "user"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Dependency to get the current user from the token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return fake_decode_token(token)


# Context manager to handle the lifespan of the application
@asynccontextmanager
async def lifespan(app: FastAPI):
    global repository_promotions
    global repository_plannings
    global repository_teachers
    global repository_courses
    global repository_rooms
    repository_promotions = None
    repository_plannings = None
    repository_teachers = None
    repository_courses = None
    repository_rooms = None
    yield


# Create the FastAPI application
app = FastAPI(lifespan=lifespan)


# Pydantic models for the API
class Promotion(BaseModel):
    id: str
    study_year: int
    diploma: str
    name: str


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
    date: str
    promotion: Promotion
    slots: List[PlanningSlot]


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Handles user login and returns an access token.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
    Returns:
        dict: A dictionary containing the access token and token type if the credentials are valid.
    HTTP Status Codes:
        200 OK: If the login is successful and the credentials are valid.
        401 Unauthorized: If the login fails due to invalid credentials.
    """
    if form_data.username == "user" and form_data.password == "password":
        return {"access_token": "fake-super-secret-token", "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")



@app.get("/api/v1/promotions", response_model=List[Promotion])
async def get_promotions() -> List[Promotion]:
    """
    Retrieve a list of promotions.
    This asynchronous function fetches all promotion entities from the repository,
    converts them to Promotion objects, and returns the list of promotions.
    Returns:
        List[Promotion]: A list of Promotion objects.
    HTTP Status Codes:
        200 OK: Successfully retrieved the list of promotions.
        500 Internal Server Error: An error occurred while fetching the promotions.
    """
    global repository_promotions
    try:
        promotion_entities = repository_promotions.find_all()
        promotions = [await get_promotion_from_entity(entity) for entity in promotion_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return promotions


@app.post("/api/v1/promotions", response_model=Promotion)
async def add_promotion(promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    """
    Add a new promotion.
    This endpoint allows authenticated users to add a new promotion to the repository.
    Args:
        promotion (Promotion): The promotion object to be added.
        user (dict, optional): The current authenticated user. This is automatically provided by the dependency injection.
    Returns:
        Promotion: The added promotion object.
    HTTP Status Codes:
        201 Created: The promotion was successfully added.
        401 Unauthorized: The user is not authenticated.
        403 Forbidden: The user does not have permission to add a promotion.
        500 Internal Server Error: An error occurred while adding the promotion.
    """

    global repository_promotions
    # Add logic to save the promotion to the repository
    return promotion


@app.put("/api/v1/promotions/{promotion_id}", response_model=Promotion)
async def update_promotion(promotion_id: str, promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    """
    Update an existing promotion.
    This endpoint allows users to update the details of an existing promotion.
    Args:
        promotion_id (str): The unique identifier of the promotion to be updated.
        promotion (Promotion): The updated promotion data.
        user (dict, optional): The current authenticated user. Defaults to the user obtained from the `get_current_user` dependency.
    Returns:
        Promotion: The updated promotion object.
    HTTP Status Codes:
        200 OK: The promotion was successfully updated.
        400 Bad Request: The request data is invalid.
        401 Unauthorized: The user is not authenticated.
        403 Forbidden: The user does not have permission to update the promotion.
        404 Not Found: The promotion with the specified ID does not exist.
    """
    global repository_promotions
    # Add logic to update the promotion in the repository
    return promotion


@app.delete("/api/v1/promotions/{promotion_id}", response_model=dict)
async def delete_promotion(promotion_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a promotion by its ID.
    Args:
        promotion_id (str): The ID of the promotion to be deleted.
        user (dict, optional): The current authenticated user. Defaults to Depends(get_current_user).
    Returns:
        dict: A message indicating the promotion has been deleted.
    HTTP Status Codes:
        200 OK: Promotion successfully deleted.
        401 Unauthorized: Authentication credentials were missing or incorrect.
        403 Forbidden: The user does not have permission to delete the promotion.
        404 Not Found: The promotion with the specified ID does not exist.
    """
    global repository_promotions
    # Add logic to delete the promotion from the repository
    return {"message": "Promotion deleted"}


@app.get("/api/v1/teachers", response_model=List[Teacher])
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
    global repository_teachers
    try:
        teacher_entities = repository_teachers.find_all()
        teachers = [await get_teacher_from_entity(entity) for entity in teacher_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return teachers


@app.post("/api/v1/teachers", response_model=Teacher)
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
    global repository_teachers
    # Add logic to save the teacher to the repository
    return teacher


@app.put("/api/v1/teachers/{teacher_id}", response_model=Teacher)
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
    global repository_teachers
    # Add logic to update the teacher in the repository
    return teacher


@app.delete("/api/v1/teachers/{teacher_id}", response_model=dict)
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
    global repository_teachers
    # Add logic to delete the teacher from the repository
    return {"message": "Teacher deleted"}


@app.get("/api/v1/courses", response_model=List[Course])
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
    global repository_courses
    try:
        course_entities = repository_courses.find_all()
        courses = [await get_course_from_entity(entity) for entity in course_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return courses


@app.post("/api/v1/courses", response_model=Course)
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
    global repository_courses
    # Add logic to save the course to the repository
    return course


@app.put("/api/v1/courses/{course_id}", response_model=Course)
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
    global repository_courses
    # Add logic to update the course in the repository
    return course


@app.delete("/api/v1/courses/{course_id}", response_model=dict)
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
    global repository_courses
    # Add logic to delete the course from the repository
    return {"message": "Course deleted"}


@app.get("/api/v1/rooms", response_model=List[Room])
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
    global repository_rooms
    try:
        room_entities = repository_rooms.find_all()
        rooms = [await get_room_from_entity(entity) for entity in room_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return rooms


@app.post("/api/v1/rooms", response_model=Room)
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
    global repository_rooms
    # Add logic to save the room to the repository
    return room


@app.put("/api/v1/rooms/{room_id}", response_model=Room)
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
    global repository_rooms
    # Add logic to update the room in the repository
    return room


@app.delete("/api/v1/rooms/{room_id}", response_model=dict)
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
    global repository_rooms
    # Add logic to delete the room from the repository
    return {"message": "Room deleted"}


@app.get("/api/v1/planning-slots", response_model=List[PlanningSlot])
async def get_planning_slots() -> List[PlanningSlot]:
    """
    Fetches all planning slots.
    This asynchronous function retrieves all planning slots from the repository and converts them into a list of PlanningSlot objects.
    Returns:
        List[PlanningSlot]: A list of planning slots.
    Raises:
        HTTPException: If an error occurs while fetching the planning slots, an HTTP 500 status code is returned.
    """
    global repository_plannings
    try:
        planning_slot_entities = repository_plannings.find_all_slots()
        planning_slots = [await get_planning_slot_from_entity(entity) for entity in planning_slot_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return planning_slots


@app.post("/api/v1/planning-slots", response_model=PlanningSlot)
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
    global repository_plannings
    # Add logic to save the planning slot to the repository
    return planning_slot


@app.put("/api/v1/planning-slots/{planning_slot_id}", response_model=PlanningSlot)
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
    global repository_plannings
    # Add logic to update the planning slot in the repository
    return planning_slot


@app.delete("/api/v1/planning-slots/{planning_slot_id}", response_model=dict)
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
    global repository_plannings
    # Add logic to delete the planning slot from the repository
    return {"message": "Planning slot deleted"}


@app.get("/api/v1/planning", response_model=List[Planning])
async def get_planning(date: str = None, promotion_id: str = None) -> List[Planning]:
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
    global repository_plannings
    try:
        if date and promotion_id:
            planning_entities = repository_plannings.find_by_date_and_promotion(dt.fromisoformat(date), domain.PromotionId(id=promotion_id))
        else:
            planning_entities = repository_plannings.find_all()
        plannings = [await get_planning_from_entity(entity) for entity in planning_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return plannings


# Helper functions to convert domain entities to Pydantic models
async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id), study_year=entity.study_year, diploma=entity.diploma, name=entity.name)


async def get_teacher_from_entity(entity: domain.Teacher) -> Teacher:
    return Teacher(id=str(entity.id), name=entity.name, firstname=entity.firstname)


async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)


async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)


async def get_planning_from_entity(entity: domain.Planning) -> Planning:
    promotion = await get_promotion_from_entity(repository_promotions.find_by_id(entity.promotion_id))
    slots = [await get_planning_slot_from_entity(slot) for slot in entity.slots]
    return Planning(id=str(entity.id), date=str(entity.date), promotion=promotion, slots=slots)


async def get_planning_slot_from_entity(entity: domain.PlanningSlot) -> PlanningSlot:
    promotion = await get_promotion_from_entity(repository_promotions.find_by_id(entity.promotion_id))
    teacher = await get_teacher_from_entity(repository_teachers.find_by_id(entity.teacher_id))
    course = await get_course_from_entity(repository_courses.find_by_id(entity.course_id))
    room = await get_room_from_entity(repository_rooms.find_by_id(entity.room_id))
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


# Helper functions to convert domain entities to Pydantic models
async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id), study_year=entity.study_year, diploma=entity.diploma, name=entity.name)


async def get_teacher_from_entity(entity: domain.Teacher) -> Teacher:
    return Teacher(id=str(entity.id), name=entity.name, firstname=entity.firstname)


async def get_course_from_entity(entity: domain.Course) -> Course:
    return Course(id=str(entity.id), name=entity.name)


async def get_room_from_entity(entity: domain.Room) -> Room:
    return Room(id=str(entity.id), name=entity.name, description=entity.description)


async def get_planning_from_entity(entity: domain.Planning) -> Planning:
    promotion = await get_promotion_from_entity(repository_promotions.find_by_id(entity.promotion_id))
    slots = [await get_planning_slot_from_entity(slot) for slot in entity.slots]
    return Planning(id=str(entity.id), date=str(entity.date), promotion=promotion, slots=slots)


async def get_planning_slot_from_entity(entity: domain.PlanningSlot) -> PlanningSlot:
    promotion = await get_promotion_from_entity(repository_promotions.find_by_id(entity.promotion_id))
    teacher = await get_teacher_from_entity(repository_teachers.find_by_id(entity.teacher_id))
    course = await get_course_from_entity(repository_courses.find_by_id(entity.course_id))
    room = await get_room_from_entity(repository_rooms.find_by_id(entity.room_id))
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
