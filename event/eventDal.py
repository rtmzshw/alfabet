from pypika import Order, Query, Table, functions
from event.eventSchema import EventCreationRequest, EVENT_TABLE
from postgrese import exec_query
from datetime import datetime
from postgrese import conn


def add_event(event: EventCreationRequest):
    eventTable = Table(EVENT_TABLE)
    query = Query.into(eventTable).columns('name', 'venue', 'date', 'popularity', 'creation_date') \
        .insert(event.name, event.venue, event.date, event.popularity, datetime.now().date())
    exec_query(query.get_sql())
