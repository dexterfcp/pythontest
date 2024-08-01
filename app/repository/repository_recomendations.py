from sqlalchemy.orm import Session
import datetime
from .. import models, schemas


def create_review(db: Session, review: schemas.LocationCategoryReviewCreate):
    db_review = models.LocationCategoryReview(location_id=review.location_id, category_id=review.category_id, last_review=review.last_review, review=review.review, rating=review.rating)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_unreviewed_locations(db: Session):
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    return db.query(models.LocationCategoryReview).filter(
        (models.LocationCategoryReview.last_review < one_month_ago) |
        (models.LocationCategoryReview.review == "")
        ).order_by(
        models.LocationCategoryReview.review == "",  # Prioriza reviews vacíos
        models.LocationCategoryReview.last_review.desc()  # Luego filtra por antigüedad
        ).limit(10).all()

