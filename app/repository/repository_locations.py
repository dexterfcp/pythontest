from sqlalchemy.orm import Session
import datetime
from .. import models, schemas


def create_location(db: Session, location: schemas.LocationCreate):
    db_location = models.Location(name=location.name, description=location.description, latitude=location.latitude, longitude=location.longitude, city=location.city)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_location_by_name(db: Session, name: str):
    return db.query(models.Location).filter(models.Location.name == name).first()
