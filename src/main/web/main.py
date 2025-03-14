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
