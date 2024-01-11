from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware
from event.eventApi import app
from event.test.eventMocks import authenticateMock, event_mock
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
import pytest
from sqlalchemy.orm import sessionmaker
import json
from user.userSchema import UserSchema
from event.eventSchema import EventSchema
from fastapi.encoders import jsonable_encoder
from utils import convert_to_point
url = URL.create(
    drivername="postgresql",
    username="postgres",
    database="postgres",
    password="alfabet"
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

Base.metadata.create_all(bind=engine)
client = None
user_id = None


# TODO list tests and no auth tests
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    clean_db(session)

    new_user = create_user(session)
    app.add_middleware(BaseHTTPMiddleware,
                       dispatch=authenticateMock(new_user.id))
    global user_id
    user_id = new_user.id

    global client
    client = TestClient(app)

    session.close()
    yield
    session = Session()
    clean_db(session)
    session.close()


@pytest.fixture(autouse=True)
def setup_and_teardown_each_test():
    Session = sessionmaker(bind=engine)
    session = Session()
    clean_events(session)
    session.close()
    yield
    session = Session()
    clean_events(session)
    session.close()


def test_post_event():
    response = client.post("/", json=event_mock)
    assert response.status_code == 200
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event = session.query(EventSchema).filter_by(
            id=response.json()["id"]).first()

        assert event_mock["name"] == event.name
        assert event_mock["popularity"] == event.popularity
        assert event_mock["venue"] == event.venue


def test_post_event_twice():
    response = client.post("/", json=event_mock)
    assert response.status_code == 200
    response = client.post("/", json=event_mock)
    assert response.status_code == 409


def test_get_event_by_id():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_id = add_event(session)
        response = client.get(f"/{str(event_id)}")
        assert response.status_code == 200
        event = response.json()
        assert event_mock["name"] == event["name"]
        assert event_mock["popularity"] == event["popularity"]
        assert event_mock["venue"] == event["venue"]


def test_get_event_dosent_exists():
    response = client.get("/12312")
    assert response.status_code == 404


def test_delete_event():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_id = add_event(session)
        response = client.delete(f"/{str(event_id)}")
        assert response.status_code == 200
        event = session.query(EventSchema).filter_by(id=event_id).first()
        assert event == None


def test_delete_event_dosent_exists():
    response = client.delete("/12312")
    assert response.status_code == 404


def test_update_event():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_id = add_event(session)
        response = client.put(f"/{str(event_id)}",
                              json={"name": "change", "popularity": 2000})
        assert response.status_code == 200
        event = session.query(EventSchema).filter_by(id=event_id).first()
        assert event.name == "change"
        assert event.popularity == 2000


def test_update_event_dosent_exists():
    response = client.put("/12312", {"name": "change", "popularity": 2000})
    assert response.status_code == 404


def clean_db(session):
    session.query(EventSchema).delete()
    session.query(UserSchema).delete()
    session.commit()


def clean_events(session):
    session.query(EventSchema).delete()
    session.commit()


def create_user(session):
    new_user = UserSchema(
        email="rtmzshw@gmail.com", password="12345678")
    session.add(new_user)
    session.commit()
    return new_user


def add_event(session):
    event_to_create = EventSchema(name=event_mock["name"], venue=event_mock["venue"], user_id=user_id,
                                  date=event_mock["date"], popularity=event_mock["popularity"],
                                  location=convert_to_point(event_mock["location"]))
    session.add(event_to_create)
    session.commit()
    event_id = event_to_create.id
    return event_id
