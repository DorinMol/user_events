from sqlalchemy.orm import Session
from app.auth.utils import get_password_hash
from app.database import models as db_models
from app.models.user import UserCreate
from app.models.event import Event


def get_by_id(db: Session, user_id: int):
    return db.query(db_models.User).filter(
        db_models.User.id == user_id).first()


def get_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(
        db_models.User.email == email).first()


def get_many(db: Session, skip: int, limit: int):
    return db.query(db_models.User).offset(skip).limit(limit).all()


def create(db: Session, user: UserCreate):
    hashed = get_password_hash(user.password)
    db_user = db_models.User(name=user.name, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Item).offset(skip).limit(limit).all()


def create_user_event(db: Session, event: Event, user_id: int):
    db_event = db_models.Item(**event.dict(), owner_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
