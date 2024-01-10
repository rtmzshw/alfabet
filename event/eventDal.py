from pypika import Query, Table, Schema
from event.eventSchema import EventSchema
from event.eventTypes import Event, EventCreationRequest, EventUpdateRequest, SortingOptions, QueryOptions
from postgrese import engine
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from utils import convert_to_point
from geoalchemy2 import functions
from typing import List
from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_Point


def add_event(event: EventCreationRequest):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_to_create = EventSchema(name=event.name, venue=event.venue,
                                      date=event.date, popularity=event.popularity, location=convert_to_point(event.location))
        session.add(event_to_create)
        session.commit()
        return event_to_create.id


def get_event(event_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event = session.query(EventSchema).filter_by(id=event_id).first()
        return event


def get_events(query_options: QueryOptions, location: List[float] | None, sorting_options: SortingOptions):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(EventSchema)
        if (query_options.venue):
            query = query.filter_by(venue=query_options.venue)

        if (location):
            point_wkb = WKTElement(convert_to_point(location), 0)
            # TODO think abkout radius
            query = query.filter(func.ST_DFullyWithin(
                EventSchema.location, point_wkb, 10))

        if sorting_options.date:
            query = query.order_by(
                EventSchema.date.asc() if sorting_options.date == 1 else EventSchema.date.desc())

        if sorting_options.popularity:
            query = query.order_by(
                EventSchema.popularity.asc() if sorting_options.popularity == 1 else EventSchema.popularity.desc())

        if sorting_options.creation_time:
            query = query.order_by(
                EventSchema.creation_date.asc() if sorting_options.creation_time == 1 else EventSchema.creation_date.desc())

        events = query.all()
        return events


def delete_event(event_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        res = session.query(EventSchema).filter_by(id=event_id).delete()
        session.commit()
        return bool(res)

# TODO try to improve any
def update_event(event_id: str, event_update_request: dict[str, any]):
    # TODO location dosent include 2 cells
    if('location' in event_update_request):
        event_update_request["location"] = convert_to_point(event_update_request["location"])
        
    Session = sessionmaker(bind=engine)
    with Session() as session:
        res = session.query(EventSchema).filter_by(
            id=event_id).update(values=event_update_request)
        session.commit()

        return bool(res)
