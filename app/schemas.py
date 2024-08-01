from pydantic import ConfigDict, BaseModel, field_validator, ValidationError
from datetime import datetime

class LocationBase(BaseModel):
    """
    This class represents a basic information about a location.

    Attributes:
        name (str): The name of the location.
        description (str): A description of the location.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        city (str): The city where the location is located.
    """
    name: str
    description: str
    latitude: float
    longitude: float
    city: str

class LocationCreate(LocationBase):
    """
    This class represents a location to be created.

    Attributes:
        latitude (float): The latitude of the location. This value must be between -90 and 90.
        longitude (float): The longitude of the location. This value must be between -180 and 180.
        city (str): The city where the location is located. This value must be between 3 and 100 characters long.
        description (str): A description of the location. This value must be between 10 and 300 characters long.
    """
    @field_validator("latitude")
    def validate_latitude(cls, v):
        """Validate latitude"""
        if v > 90 or v < -90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        """Validate longitude"""
        if v > 180 or v < -180:
            raise ValueError("Longitude must be between -180 and 180")
        return v
    
    @field_validator("city")
    def validate_city(cls, v):
        """Validate city"""
        if len(v) < 3 and len(v) > 100:
            raise ValueError("City must be at least 3 characters long and no more than 100 characters long" )
        return v
    
    @field_validator("description")
    def validate_description(cls, v):
        """Validate description"""
        if len(v) < 10 and len(v) > 300:
            raise ValueError("Description must be at least 10 characters long and no more than 300 characters long" )
        return v

class Location(LocationBase):
    """
    Represents a location object.

    Attributes:
        id (int): The unique identifier of the location.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)


class CategoryBase(BaseModel):
    """
    Represents a category base object.

    Attributes:
        name (str): The name of the category.
        description (str): A description of the category.
    """
    name: str
    """The name of the category."""

    description: str
    """A description of the category."""

class CategoryCreate(CategoryBase):
    """
    Represents a category create object.

    Attributes:
        name (str): The name of the category. This value must be between 3 and 100 characters long.
        description (str): A description of the category. This value must be between 10 and 300 characters long.
    """
    @field_validator("name")
    def validate_name(cls, v):
        """
        Validates the name of the category.

        Args:
            v (str): The name of the category.

        Raises:
            ValueError: If the name is not between 3 and 100 characters long.

        Returns:
            str: The validated name of the category.
        """
        if len(v) < 3 and len(v) > 100:
            raise ValueError("Name must be at least 3 characters long and no more than 100 characters long" )
        return v

    @field_validator("description")
    def validate_description(cls, v):
        """
        Validates the description of the category.

        Args:
            v (str): The description of the category.

        Raises:
            ValueError: If the description is not between 10 and 300 characters long.

        Returns:
            str: The validated description of the category.
        """
        if len(v) < 10 and len(v) > 300:
            raise ValueError("Description must be at least 10 characters long and no more than 300 characters long" )
        return v

class Category(CategoryBase):
    """
    Represents a category object.

    Attributes:
        id (int): The unique identifier of the category.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)

class LocationCategoryReviewBase(BaseModel):
    """
    Represents the base attributes of a location category review.

    Attributes:
        location_id (int): The unique identifier of the location.
        category_id (int): The unique identifier of the category.
        last_review (datetime): The last review date for the location category.
        review (str): The review text for the location category.
        rating (float): The rating for the location category.
    """
    location_id: int
    """ The unique identifier of the location. """
    category_id: int
    """ The unique identifier of the category. """
    last_review: datetime
    """ The last review date for the location category. """
    review: str
    """ The review text for the location category. """
    rating: float
    """ The rating for the location category. """

class LocationCategoryReviewCreate(LocationCategoryReviewBase):
    """
    Represents a location category review to be created.

    Attributes:
        location_id (int): The unique identifier of the location.
        category_id (int): The unique identifier of the category.
        rating (float): The rating for the location category.
        review (str): The review text for the location category.
    """

    @field_validator("location_id")
    def validate_location_id(cls, v):
        """
        Validates the location ID.

        Args:
            v (int): The location ID.

        Raises:
            ValueError: If the location ID is null or less than 0.

        Returns:
            int: The validated location ID.
        """
        if v is None or v < 0:
            raise ValueError("Location ID must be greater than or equal to 0")
        return v

    @field_validator("category_id")
    def validate_category_id(cls, v):
        """
        Validates the category ID.

        Args:
            v (int): The category ID.

        Raises:
            ValueError: If the category ID is null or less than 0.

        Returns:
            int: The validated category ID.
        """
        if v is None or v < 0:
            raise ValueError("Category ID must be greater than or equal to 0")
        return v

    @field_validator("rating")
    def validate_rating(cls, v):
        """
        Validates the rating.

        Args:
            v (float): The rating.

        Raises:
            ValueError: If the rating is less than 0 or greater than 5.

        Returns:
            float: The validated rating.
        """
        if v < 0 or v > 5:
            raise ValueError("Rating must be between 0 and 5")
        return v

    @field_validator("review")
    def validate_review(cls, v):
        """
        Validates the review.

        Args:
            v (str): The review.

        Raises:
            ValueError: If the review is less than 10 characters or more than 300 characters.

        Returns:
            str: The validated review.
        """
        if len(v) < 10 and len(v) > 300:
            raise ValueError("Review must be at least 10 characters long and no more than 300 characters long" )
        return v

class LocationCategoryReview(LocationCategoryReviewBase):
    """
    Represents a location category review.

    Attributes:
        id (int): The unique identifier of the location category review.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)
