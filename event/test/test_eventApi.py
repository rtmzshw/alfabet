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
from event.test.helpers import add_event, clean_db, clean_events
from user.test.helpers import create_user
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
        event_id = add_event(session, user_id)
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
        event_id = add_event(session, user_id)
        response = client.delete(f"/{str(event_id)}")
        assert response.status_code == 200
        event = session.query(EventSchema).filter_by(id=event_id).first()
        assert event == None


def test_delete_event_not_mine():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_user = create_user(session, "rtmzshw2@gmail.com")
        event_id = add_event(session, new_user.id, "name")
        response = client.delete(f"/{event_id}")
        assert response.status_code == 401


def test_delete_event_dosent_exists():
    response = client.delete("/12312")
    assert response.status_code == 404


def test_update_event():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        event_id = add_event(session, user_id)
        response = client.put(f"/{str(event_id)}",
                              json={"name": "change", "popularity": 2000})
        assert response.status_code == 200
        event = session.query(EventSchema).filter_by(id=event_id).first()
        assert event.name == "change"
        assert event.popularity == 2000


def test_update_event_not_mine():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_user = create_user(session, "rtmzshw3@gmail.com",)
        event_id = add_event(session, new_user.id, "name")
        response = client.put(
            f"/{event_id}", json={"name": "change", "popularity": 2000})
        assert response.status_code == 401


def test_update_event_dosent_exists():
    response = client.put(
        "/12312", json={"name": "change", "popularity": 2000})
    assert response.status_code == 404


def test_empty_update():
    response = client.put("/12312", json={})
    assert response.status_code == 400


def test_search():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        add_event(session, user_id, name="A", date="2024-01-12T10:45:00+02:00",
                  location=[15, 5], venue="place1", popularity=200,)
        add_event(session, user_id, name="B", date="2024-01-13T10:45:00+02:00",
                  location=[15, 5], venue="place1", popularity=1000,)
        add_event(session, user_id, name="C", date="2024-01-14T10:45:00+02:00",
                  location=[50, 5], venue="place2", popularity=400,)
        add_event(session, user_id, name="D", date="2024-01-15T10:45:00+02:00",
                  location=[50, 5], venue="place2", popularity=500,)

        response = client.get(f"/search?venue=place1&popularity=-1")
        data = response.json()
        assert data[0]["name"] == "B"
        assert data[1]["name"] == "A"

        response = client.get(f"/search?venue=place2&date=1")
        data = response.json()
        assert data[0]["name"] == "C"
        assert data[1]["name"] == "D"

        response = client.get(f"/search?location=16&location=5&popularity=1")
        data = response.json()
        assert data[0]["name"] == "A"
        assert data[1]["name"] == "B"

        response = client.get(f"/search?location=1&location=5&popularity=1")
        data = response.json()
        assert len(data) == 0

        response = client.get(f"/search")
        data = response.json()
        assert len(data) == 4
