from event.eventSchema import EventSchema
from user.userSchema import UserSchema
from utils import convert_to_point
from event.test.eventMocks import event_mock


def clean_db(session):
    session.query(EventSchema).delete()
    session.query(UserSchema).delete()
    session.commit()


def clean_events(session):
    session.query(EventSchema).delete()
    session.commit()


def add_event(session, user_id: str,
              name: str = event_mock["name"],
              venue: str = event_mock["venue"],
              date: str = event_mock["date"],
              popularity: int = event_mock["popularity"],
              location: list[float] = event_mock["location"]
              ):
    event_to_create = EventSchema(name=name, venue=venue, user_id=user_id,
                                  date=date, popularity=popularity,
                                  location=convert_to_point(location))
    session.add(event_to_create)
    session.commit()
    event_id = event_to_create.id
    return event_id
