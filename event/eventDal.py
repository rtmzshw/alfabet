from pypika import Query, Table, Schema
from event.eventSchema import EventSchema
from notification.notificationSchema import NotificationSchema
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
from errors import Unauthorized, NotFound
from datetime import datetime, timedelta
from notification.notificationLogic import calc_notification_timing
from event.eventConfig import default_query_radius


def add_event(event: EventCreationRequest, user_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_to_create = EventSchema(name=event.name, venue=event.venue, user_id=user_id,
                                      date=event.date, popularity=event.popularity, location=convert_to_point(event.location))
        session.add(event_to_create)
        notification = NotificationSchema(description="example: should be recived from user, due to time constraints its hardcoded",
                                          date=calc_notification_timing(event.date), event_id=event_to_create.id)
        session.add(notification)
        session.commit()
        return event_to_create.id


def get_event(event_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event = session.query(EventSchema).filter_by(id=event_id).first()
        return event


def get_events(query_options: QueryOptions, location: List[float] | None, sorting_options: SortingOptions):
    # TODO refactor this into map
    Session = sessionmaker(bind=engine)
    with Session() as session:
        query = session.query(EventSchema)
        if (query_options.venue):
            query = query.filter_by(venue=query_options.venue)

        if (location):
            point_wkb = WKTElement(convert_to_point(location), 0)
            query = query.filter(func.ST_DFullyWithin(
                EventSchema.location, point_wkb, default_query_radius))

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


def delete_event(event_id: str, user_id: str):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event = session.query(EventSchema).filter_by(id=event_id).first()
        if not event:
            raise NotFound()

        if event.user_id != user_id:
            raise Unauthorized()

        session.query(EventSchema).filter_by(id=event_id).delete()
        session.commit()


def update_event(event_id: str, event_update_request: dict[str, any], user_id: int):
    if ('location' in event_update_request):
        event_update_request["location"] = convert_to_point(
            event_update_request["location"])

    Session = sessionmaker(bind=engine)
    with Session() as session:
        event = session.query(EventSchema).filter_by(id=event_id).first()
        if not event:
            raise NotFound()

        if event.user_id != user_id:
            raise Unauthorized()
        for key in event_update_request:
            setattr(event, key, event_update_request[key])
            
        session.commit()
