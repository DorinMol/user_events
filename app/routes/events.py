from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from ..models.event import Event, EventCreate, EventUpdate
from ..models.user import User, UserRoleEnum
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
async def get_all(skip: int = 0, limit: int = 10,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    if current_user.role == UserRoleEnum.admin:
        return event.get_events(db, skip, limit)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")


@router.get('/{owner_id}',
            status_code=status.HTTP_200_OK,
            response_model=List[Event])
async def get_by_owner(owner_id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return event.get_events_by_owner(db, owner_id)


@router.post('/', response_model=Event)
async def create(eventIn: EventCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)):
    eventIn.owner_id = current_user.id
    db_event = event.create_event(db, eventIn)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return db_event


@router.delete('/{event_id}', response_model=Event)
async def delete(event_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)):
    db_event = event.delete_event(db, event_id, current_user.id)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return db_event


@router.put('/', response_model=Event)
async def update(eventIn: EventUpdate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)):
    db_event = event.update_event(db, eventIn, current_user.id)
    if db_event is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return db_event
