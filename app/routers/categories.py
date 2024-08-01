from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..repository import repository_categories
from .. import models, schemas, database

router = APIRouter()

@router.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate):
    """
    Creates a new category in the database.

    Args:
        category (schemas.CategoryCreate): The category object containing the name and description of the new category.

    Returns:
        schemas.Category: The newly created category object.

    Errors:
        HTTPException: If the category already exists in the database.
    """
    db = database.SessionLocal()
    return repository_categories.create_category(db, category)

@router.get("/categories/", response_model=List[schemas.Category])
def get_categories():
    """
    Retrieves a list of categories from the database.

    This function uses the FastAPI router to handle a GET request to the "/categories/" endpoint.
    It returns a list of Category objects, which are serialized using the response_model parameter.

    Returns:
        List[schemas.Category]: A list of Category objects representing the categories in the database.
    """
    db = database.SessionLocal()
    return repository_categories.get_categories(db)

@router.get("/categories/{category_id}", response_model=schemas.Category)
def get_category(category_id: int):
    """
    Retrieves a category from the database based on the provided category ID.

    Args:
        category_id (int): The ID of the category to retrieve.

    Returns:
        schemas.Category: The category object matching the provided ID.

    Raises:
        HTTPException: If the category with the provided ID is not found in the database.
    """
    db = database.SessionLocal()
    category = repository_categories.get_category(db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.get("/categories/name/{category_name}", response_model=schemas.Category)
def get_category_by_name(category_name: str):
    """
    Retrieves a category from the database based on the provided category name.

    Args:
        category_name (str): The name of the category to retrieve.

    Returns:
        schemas.Category: The category object matching the provided name.

    Raises:
        HTTPException: If the category with the provided name is not found in the database.
    """
    db = database.SessionLocal()
    category = repository_categories.get_category_by_name(db, category_name=category_name)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category