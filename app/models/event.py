from typing import Optional

from pydantic import BaseModel


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None


class EventCreate(EventBase):
    owner_id: int


class Event(EventCreate):
    id: int

    class Config:
        orm_mode = True
