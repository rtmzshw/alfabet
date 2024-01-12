from datetime import datetime
from pydantic import BaseModel


class SubsciptionCreationRequest(BaseModel):
    event_id = str


class User(SubsciptionCreationRequest):
    id: int
    user_id: str
    creation_date: datetime
