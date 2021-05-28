from sqlalchemy.orm import Session
from app.auth.utils import get_password_hash
from app.database import models as db_models
from app.models.user import UserCreate, UserRoleEnum, UserUpdate
from app.models.event import Event
from typing import List, Optional


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


def remove_by_id(db: Session, user_id: int):
    try:
        user = db.query(db_models.User).get(user_id)
        if user is None:
            return None
        db.delete(user)
        db.commit()
    except Exception as ex:
        print("Exception while deleting: ", ex)
    else:
        print("Deleted successfully")
        return user


def _update_helper(user: db_models.User,
                   name: Optional[str]):
    if name is not None:
        user.name = name
    return user


def update_self(db: Session, user_to_update: UserUpdate):
    user = db.query(db_models.User).get(user_to_update.id)
    if user is None:
        return None
    user = _update_helper(user, user_to_update.name)
    if user_to_update.password is not None and len(user_to_update.password) > 3:
        hashed = get_password_hash(user_to_update.password)
        user.password = hashed
    db.commit()
    return user


def update_other(db: Session, user_to_update: UserUpdate):
    user = db.query(db_models.User).get(user_to_update.id)
    if user is None:
        return None
    user = _update_helper(user, user_to_update.name)
    if user_to_update.role is not None:
        user.role = user_to_update.role
    db.commit()
    return user
