from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..repository import repository_locations
from .. import models, schemas, database

router = APIRouter()

@router.post("/locations/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate):
    """
    Creates a new location in the database.

    Args:
        location (schemas.LocationCreate): The location to be created.

    Returns:
        schemas.Location: The created location.
    """
    db = database.SessionLocal()
    return repository_locations.create_location(db, location)

@router.get("/locations/", response_model=List[schemas.Location])
def get_locations():
    """
    Retrieves a list of locations from the database.

    Returns:
        List[schemas.Location]: A list of locations.
    """
    db = database.SessionLocal()
    return repository_locations.get_locations(db)

@router.get("/locations/{location_id}", response_model=schemas.Location)
def get_location(location_id: int):
    """
    Retrieves a location from the database based on the provided location ID.

    Parameters:
        location_id (int): The ID of the location to retrieve.

    Returns:
        schemas.Location: The location object if found, otherwise raises an HTTPException with a status code of 404 and a detail message of "Location not found".
    """
    db = database.SessionLocal()
    location = repository_locations.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

@router.get("/locations/name/{name}", response_model=schemas.Location)
def get_location_by_name(name: str):
    """
    Retrieves a location from the database based on the provided name.

    Args:
        name (str): The name of the location to retrieve.

    Returns:
        schemas.Location: The location object if found, otherwise raises an HTTPException with a status code of 404 and a detail message of "Location not found".
    """
    db = database.SessionLocal()
    location = repository_locations.get_location_by_name(db, name=name)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location
