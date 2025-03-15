"""
This module serves as the main entry point for the FastAPI application.
It initializes the FastAPI app with a custom lifespan context manager to set up
and tear down application state. The application includes routers for various
functionalities such as authentication, promotions, teachers, courses, rooms,
and planning.
Modules included:
- auth: Handles authentication-related endpoints.
- promotions: Manages promotion-related endpoints.
- teachers: Manages teacher-related endpoints.
- courses: Manages course-related endpoints.
- rooms: Manages room-related endpoints.
- planning: Manages planning-related endpoints.
The `lifespan` context manager initializes repository states to `None` at the
start of the application and ensures proper cleanup when the application shuts
down.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.main.web import auth, promotions, teachers, courses, rooms, planning
from src.main.web import state


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.repository_promotions = None
    state.repository_plannings = None
    state.repository_teachers = None
    state.repository_courses = None
    state.repository_rooms = None
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth.router)
app.include_router(promotions.router)
app.include_router(teachers.router)
app.include_router(courses.router)
app.include_router(rooms.router)
app.include_router(planning.router)
