from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import List, Union, Tuple
from typing import TypedDict


def validate_point(value: List[float]):
    if len(value) < 2:
        raise ValueError("location is an array with two values")
    return value


class EventCreationRequest(BaseModel):
    name: str
    venue: str
    date: datetime
    location: List[float]
    popularity: int

    _validate_location = field_validator("location")(validate_point)


class Event(EventCreationRequest):
    id: int
    creation_date: datetime
    location: List[float]


class EventUpdateRequest(EventCreationRequest):
    name: str | None = None
    venue: str | None = None
    date: datetime | None = None
    popularity: int | None = None
    location: List[float] | None = None

    _validate_location = field_validator("location")(validate_point)
    
class QueryOptions(BaseModel):
    venue: str | None = None
    date: int | None = None
    popularity: int | None = None
    creation_time: int | None = None


class Id(BaseModel):
    id:int


class Ok(BaseModel):
    ok: bool


class SubscriptionStatus(BaseModel):
    status: str
