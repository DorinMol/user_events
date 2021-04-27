from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from ..models.user import UserAuth
from ..auth.auth import create_access_token, authenticate_user
from ..database.crud.users import get_by_email
from ..database.database import SessionLocal


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(tags=['auth'])


@router.post("/token", response_model=Token)
async def login(user: UserAuth, db: SessionLocal = Depends(get_db)):
    db_user = get_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Data")
    is_auth = authenticate_user(db_user.password, user.password)
    if not is_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ivalid data.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(db_user.email)
    return {"access_token": access_token, "token_type": "bearer"}
