from pydantic import BaseModel
from datetime import date as dateType
from pypika import Query, Column
from postgrese import conn, exec_query

EVENT_TABLE = 'events'

class EventCreationRequest(BaseModel):
    name: str
    venue:str
    date: dateType
    popularity: int
    
class Event(EventCreationRequest):
    id: str
    name: str
    venue:str
    date: dateType
    popularity: int
    creationDate: dateType


def create_events_table():
    try:
        stmt:str = Query \
        .create_table(EVENT_TABLE) \
        .columns(
            Column("id", "SERIAL", nullable=False),
            Column("name", "VARCHAR(100)", nullable=False),
            Column("venue", "VARCHAR(100)", nullable=False),
            Column("date", "DATE", nullable=False),
            Column("popularity", "INT", nullable=False),
            Column("creation_date", "DATE")) \
        .unique("name", "venue", "date") \
        .primary_key("id")

        exec_query(stmt.get_sql())

    except Exception as e:
        print(e)