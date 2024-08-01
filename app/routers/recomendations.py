from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..repository import repository_recomendations
from .. import models, schemas, database

router = APIRouter()


@router.post("/recomendations/", response_model=schemas.LocationCategoryReview)
def create_recomendation(recomendation: schemas.LocationCategoryReviewCreate):
    """
    Creates a new recommendation in the database.

    Args:
        recommendation (schemas.LocationCategoryReviewCreate): The recommendation object containing the location ID, category ID, rating, and review.

    Returns:
        schemas.LocationCategoryReview: The newly created recommendation object.

    Raises:
        HTTPException: If there is an error creating the recommendation in the database.
    """
    db = database.SessionLocal()
    return repository_recomendations.create_review(db, recomendation)

@router.get("/recomendations/unreviewed", response_model=List[schemas.LocationCategoryReview])
def get_recomendations():
    """
    Retrieves a list of unreviewed location category reviews from the database.

    This function uses the FastAPI router to handle a GET request to the "/recomendations/unreviewed" endpoint.
    It returns a list of LocationCategoryReview objects representing the unreviewed location category reviews in the database.

    Parameters:
        db (Session): The database session object. Defaults to the Session object obtained from the database.SessionLocal dependency.

    Returns:
        List[schemas.LocationCategoryReview]: A list of LocationCategoryReview objects representing the unreviewed location category reviews in the database.
    """
    db = database.SessionLocal()
    return repository_recomendations.get_unreviewed_locations(db)


