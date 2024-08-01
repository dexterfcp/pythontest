from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from .database import Base

## Pandemic Models ORM

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(300), index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String(100), index=True)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(300), index=True)

class LocationCategoryReview(Base):
    __tablename__ = "location_category_reviews"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    last_review = Column(DateTime, default=func.now(), nullable=False)
    review = Column(String(300), index=True, nullable=True)
    rating = Column(Float, nullable=True)
    location= relationship("Location")
    category = relationship("Category")