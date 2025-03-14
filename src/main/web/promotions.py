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
    Returns:
        List[Promotion]: A list of Promotion objects.
    HTTP Status Codes:
        200 OK: Successfully retrieved the list of promotions.
        500 Internal Server Error: An error occurred while fetching the promotions.
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
    # Add logic to save the promotion to the repository
    return promotion

@router.put("/{promotion_id}", response_model=Promotion)
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
    # Add logic to update the promotion in the repository
    return promotion

@router.delete("/{promotion_id}", response_model=dict)
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
    # Add logic to delete the promotion from the repository
    return {"message": "Promotion deleted"}

async def get_promotion_from_entity(entity: domain.Promotion) -> Promotion:
    return Promotion(id=str(entity.id), study_year=entity.study_year, diploma=entity.diploma, name=entity.name)
