from pypika import Query, Table, Schema
from event.eventSchema import EVENT_TABLE
from event.eventTypes import Event, EventCreationRequest
from postgrese import exec_query
from datetime import datetime
from postgrese import conn


def add_event(event: EventCreationRequest):
    eventTable = Table(EVENT_TABLE)
    query = Query.into(eventTable).columns('name', 'venue', 'date', 'popularity', 'creation_date') \
        .insert(event.name, event.venue, event.date, event.popularity, datetime.now().date())

    # Note- there is no way to add it using pypika, its a known requested feature
    query_with_return = query.get_sql() + " RETURNING id"

    res = exec_query(query_with_return)
    id = res[0]
    return id

def get_event(event_id: str):
    event_table = Table(EVENT_TABLE)
    query = Query.from_(event_table).select('*').where(
            event_table.id == event_id,
        )
    res = exec_query(query.get_sql())
    print("asdasd", res[1], res[2],res[3],res[4])
    a = EventCreationRequest(res[1], res[2],res[3],res[4])
    event = Event(a,res[0],res[5])
    return event
