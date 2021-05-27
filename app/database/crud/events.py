from app.database import models as db_models
from app.models.event import EventCreate
from sqlalchemy.orm import Session


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Item).offset(skip).limit(limit).all()


def create_user_event(db: Session, event: EventCreate):
    db_event = db_models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
