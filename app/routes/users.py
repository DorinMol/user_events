from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from ..models.user import User, UserCreate
from ..database.database import SessionLocal
from ..database.crud import users as user
from sqlalchemy.orm import Session
from ..auth.auth import get_current_active_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[User])
async def get_users(skip: int = 0,
                    limit: int = 10,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    print("current_user: ", current_user)
    return user.get_many(db, skip, limit)


@router.post('/', response_model=User)
async def create_user(userIn: UserCreate, db: Session = Depends(get_db)):
    db_user = user.get_by_email(db, userIn.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return user.create(db, userIn)


@router.delete('/', response_model=User)
async def remove_user(user_id: int,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    db_user = user.get_by_email(db, userIn.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return user.create(db, userIn)
