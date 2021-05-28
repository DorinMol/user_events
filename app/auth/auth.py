from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from .utils import verify_password
from ..database.crud.users import get_by_id
from app.database.models import User as DBUser
from ..database.database import SessionLocal
from ..models.user import User
from sqlalchemy.orm import Session
import configparser


config = configparser.ConfigParser()
config.read('.env.example')

SECRET_KEY = config["JWT"]["SECRET_KEY"]
ALGORITHM = config["JWT"]["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(config["JWT"]["ACCESS_TOKEN_EXPIRE_MINUTES"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TokenData(BaseModel):
    user_id: Optional[int] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(password: str, password_to_check: str):
    return verify_password(password_to_check, password)


def create_access_token(db_user: DBUser):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": str(db_user.id), "role": str(db_user.role.value)}
    to_encode = data.copy()
    if access_token_expires:
        expire = datetime.utcnow() + access_token_expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
