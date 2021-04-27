from typing import List
from pydantic import BaseModel

from .event import Event


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

    class Config:
        orm_mode = True
