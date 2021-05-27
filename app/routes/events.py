from fastapi import APIRouter, status, Depends
from typing import List
from ..models.event import Event, EventCreate
from ..models.user import User
from app.database.crud import events as event
from ..database.database import SessionLocal
from sqlalchemy.orm import Session
from ..auth.auth import get_current_active_user


router = APIRouter(
    prefix='/events',
    tags=['events']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[Event])
async def get_events(skip: int = 0, limit: int = 10,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    return event.get_events(db, skip, limit)


@router.post('/', response_model=Event)
async def create_event(eventIn: EventCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    return event.create_user_event(db, eventIn)
