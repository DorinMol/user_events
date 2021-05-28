from app.database import models as db_models
from app.models.event import EventCreate, EventUpdate
from sqlalchemy.orm import Session


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Event).offset(skip).limit(limit).all()


def get_events_by_owner(db: Session, owner_id: int):
    return db.query(db_models.Event).filter(db_models.Event.owner_id == owner_id).all()


def create_event(db: Session, event: EventCreate):
    try:
        db_event = db_models.Event(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
    except Exception as e:
        print("Exception while creating event...", e)
        return None
    else:
        return db_event


def delete_event(db: Session, id: int, used_id: int):
    try:
        event = db.query(db_models.Event).get(id)
        if event is None or event.owner_id != used_id:
            return None
        db.delete(event)
        db.commit()
    except Exception as ex:
        print("Exception while deleting: ", ex)
    else:
        print("Deleted successfully")
        return event


def update_event(db: Session, event_to_update: EventUpdate, user_id: int):
    event = db.query(db_models.Event).get(event_to_update.id)
    if event is None or event.owner_id != user_id:
        return None
    if event_to_update.title is not None:
        event.title = event_to_update.title
    if event_to_update.content is not None:
        event.content = event_to_update.content
    if event_to_update.description is not None:
        event.description = event_to_update.description
    db.commit()
    return event
