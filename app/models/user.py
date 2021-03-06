from typing import List, Optional
from pydantic import BaseModel
from enum import auto
from fastapi_utils.enums import StrEnum
from .event import Event


class UserRoleEnum(StrEnum):
    admin = auto()
    user = auto()


class UserBase(BaseModel):
    email: str


class UserBaseWithName(UserBase):
    name: str


class UserCreate(UserBaseWithName):
    password: str


class UserAuth(UserBase):
    password: str


class User(UserBaseWithName):
    id: int
    events: List[Event] = []
    role: UserRoleEnum

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    name: Optional[str]
    role: Optional[UserRoleEnum]
    password: Optional[str]
