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


async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id))
