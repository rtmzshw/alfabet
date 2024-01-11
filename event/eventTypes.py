from datetime import datetime
from pydantic import BaseModel
from typing import Annotated
from typing import List, Union, Tuple
from fastapi import Query

class EventCreationRequest(BaseModel):
    name: str
    venue: str
    date: datetime
    location: List[float]
    popularity: int

class Event(EventCreationRequest):
    id: int
    creation_date: datetime
    location: str



class EventUpdateRequest(EventCreationRequest):
    name: str | None = None
    venue: str | None = None
    date: datetime | None = None
    popularity: int | None = None
    location: tuple | None = None


class QueryOptions(BaseModel):
    venue: str | None = None


class SortingOptions(BaseModel):
    date: int | None = None
    popularity: int | None = None
    creation_time: int | None = None
