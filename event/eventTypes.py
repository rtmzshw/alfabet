from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import Annotated
from typing import List, Union, Tuple
from fastapi import Query


def validate_point(_, value: List[float]):
    if len(value) < 2:
        raise ValueError("location is a point of (x,y)")
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
    location: str


class EventUpdateRequest(EventCreationRequest):
    name: str | None = None
    venue: str | None = None
    date: datetime | None = None
    popularity: int | None = None
    location: List[float] | None = None

    _validate_location = field_validator("location")(validate_point)


class QueryOptions(BaseModel):
    venue: str | None = None


class SortingOptions(BaseModel):
    date: int | None = None
    popularity: int | None = None
    creation_time: int | None = None


class Id(BaseModel):
    id: int
class Ok(BaseModel):
    ok: bool