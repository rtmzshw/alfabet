from datetime import date as dateType
from pydantic import BaseModel
import json

class EventCreationRequest(BaseModel):
    def __init__(self, name: str, venue: str, date: dateType, popularity: int):
        super().__init__()
        self.name = name
        self.venue = venue
        self.date = date
        self.popularity = popularity
        
    name: str
    venue: str
    date: dateType
    popularity: int

class Event(EventCreationRequest):
    def __init__(self, eventCreationReq: EventCreationRequest, id: str, creation_date: dateType):
        super().__init__(eventCreationReq.name,eventCreationReq.venue, eventCreationReq.date,eventCreationReq.popularity )
        self.id = id
        self.creation_date = creation_date

    id: str
    creation_date: dateType

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    # def fromArrayToJson(properties):
    #     return {'id': properties[0],
    #             'name': properties[1],
    #             'venue': properties[2],
    #             'date': properties[2],
    #             'popularity': properties[2],
    #             'creation_date': properties[2]}
