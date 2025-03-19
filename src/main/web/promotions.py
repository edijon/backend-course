"""
This module contains the implementation of the REST API for the promotions
endpoint using FastAPI. It exposes endpoints for listing all promotions,
fetching a promotion by ID, creating a new promotion, updating an existing
promotion, and deleting a promotion.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.main import domain
from src.main.web.auth import get_current_user
from src.main.web import state
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1/promotions", tags=["Promotions"])


class Promotion(BaseModel):
    id: str
    study_year: int
    diploma: str
    name: str


@router.get("", response_model=List[Promotion])
async def get_promotions() -> List[Promotion]:
    """
    Retrieve a list of promotions.
    This asynchronous function fetches all promotion entities from the repository,
    converts them to Promotion objects, and returns the list of promotions.
    """
    try:
        promotion_entities = state.repository_promotions.find_all()
        promotions = [await get_promotion_from_entity(entity) for entity in promotion_entities]
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex))
    return promotions


@router.post("", response_model=Promotion)
async def add_promotion(promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    """
    Add a new promotion.
    This endpoint allows authenticated users to add a new promotion to the repository.
    """
    # Add logic to save the promotion to the repository
    return promotion


@router.put("/{promotion_id}", response_model=Promotion)
async def update_promotion(promotion_id: str, promotion: Promotion, user: dict = Depends(get_current_user)) -> Promotion:
    """
    Update an existing promotion.
    This endpoint allows users to update the details of an existing promotion.
    """
    # Add logic to update the promotion in the repository
    return promotion


@router.delete("/{promotion_id}", response_model=dict)
async def delete_promotion(promotion_id: str, user: dict = Depends(get_current_user)) -> dict:
    """
    Delete a promotion by its ID.
    """
    # Add logic to delete the promotion from the repository
    return {"message": "Promotion deleted"}


async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id), study_year=entity.study_year, diploma=entity.diploma, name=entity.name)
