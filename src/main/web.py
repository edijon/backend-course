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


# Endpoint to get an access token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "user" and form_data.password == "password":
        return {"access_token": "fake-super-secret-token", "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Endpoint to get all promotions
@app.get("/api/v1/promotions", response_model=List[Promotion])
async def get_promotions() -> List[Promotion]:
    global repository_promotions
    try:
        promotion_entities = repository_promotions.find_all()
        promotions = [await get_promotion_from_entity(entity) for entity in promotion_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return promotions


# Endpoint to add a new promotion (requires authentication)
@app.post("/api/v1/promotions", response_model=Promotion)
async def add_promotion(promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    global repository_promotions
    # Add logic to save the promotion to the repository
    return promotion


# Endpoint to update a promotion (requires authentication)
@app.put("/api/v1/promotions/{promotion_id}", response_model=Promotion)
async def update_promotion(promotion_id: str, promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    global repository_promotions
    # Add logic to update the promotion in the repository
    return promotion

# Endpoint to delete a promotion (requires authentication)
@app.delete("/api/v1/promotions/{promotion_id}", response_model=dict)
async def delete_promotion(promotion_id: str, user: dict = Depends(get_current_user)) -> dict:
    global repository_promotions
    # Add logic to delete the promotion from the repository
    return {"message": "Promotion deleted"}

# Endpoint to get all teachers
@app.get("/api/v1/teachers", response_model=List[Teacher])
async def get_teachers() -> List[Teacher]:
    global repository_teachers
    try:
        teacher_entities = repository_teachers.find_all()
        teachers = [await get_teacher_from_entity(entity) for entity in teacher_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return teachers

# Endpoint to add a new teacher (requires authentication)
@app.post("/api/v1/teachers", response_model=Teacher)
async def add_teacher(teacher: Teacher, user: dict = Depends(get_current_user)) -> Teacher:
    global repository_teachers
    # Add logic to save the teacher to the repository
    return teacher

# Endpoint to update a teacher (requires authentication)
@app.put("/api/v1/teachers/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: str, teacher: Teacher, user: dict = Depends(get_current_user)) -> Teacher:
    global repository_teachers
    # Add logic to update the teacher in the repository
    return teacher

# Endpoint to delete a teacher (requires authentication)
@app.delete("/api/v1/teachers/{teacher_id}", response_model=dict)
async def delete_teacher(teacher_id: str, user: dict = Depends(get_current_user)) -> dict:
    global repository_teachers
    # Add logic to delete the teacher from the repository
    return {"message": "Teacher deleted"}

# Endpoint to get all courses
@app.get("/api/v1/courses", response_model=List[Course])
async def get_courses() -> List[Course]:
    global repository_courses
    try:
        course_entities = repository_courses.find_all()
        courses = [await get_course_from_entity(entity) for entity in course_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return courses


# Endpoint to add a new course (requires authentication)
@app.post("/api/v1/courses", response_model=Course)
async def add_course(course: Course, user: dict = Depends(get_current_user)) -> Course:
    global repository_courses
    # Add logic to save the course to the repository
    return course


# Endpoint to update a course (requires authentication)
@app.put("/api/v1/courses/{course_id}", response_model=Course)
async def update_course(course_id: str, course: Course, user: dict = Depends(get_current_user)) -> Course:
    global repository_courses
    # Add logic to update the course in the repository
    return course


# Endpoint to delete a course (requires authentication)
@app.delete("/api/v1/courses/{course_id}", response_model=dict)
async def delete_course(course_id: str, user: dict = Depends(get_current_user)) -> dict:
    global repository_courses
    # Add logic to delete the course from the repository
    return {"message": "Course deleted"}


# Endpoint to get all planning
@app.get("/api/v1/planning", response_model=List[Planning])
async def get_planning(date: str = None, promotion_id: str = None) -> List[Planning]:
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
