from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from ..models.user import User, UserCreate, UserRoleEnum, UserUpdate
from ..database.database import SessionLocal
from ..database.crud import users as user
from ..database.models import User as DBUser
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
    return user.get_many(db, skip, limit)


@router.post('/', response_model=User)
async def create_user(userIn: UserCreate, db: Session = Depends(get_db)):
    db_user: DBUser = user.get_by_email(db, userIn.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return user.create(db, userIn)


@router.delete('/{user_id}', response_model=User)
async def remove_user(user_id: int,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    print("current_user: ", current_user)

    if current_user.role is not UserRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden.")
    db_user = user.remove_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return db_user


@router.put('/', response_model=User)
async def update_user(user_to_update: UserUpdate,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    '''
    Update specified user_id only if current user has admin rights
    '''
    # check if update is for the current user
    # if true then allow to change events / name
    if current_user.id == user_to_update.id:
        db_user = user.update_self(db, user_to_update)
        return db_user
    if current_user.role is not UserRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden.")
    db_user = user.update_other(db, user_to_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request.")
    return db_user
