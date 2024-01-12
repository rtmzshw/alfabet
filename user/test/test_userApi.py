from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware
from user.userApi import app
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
import pytest
from sqlalchemy.orm import sessionmaker
from user.userSchema import UserSchema
from user.userUtils import verify_jwt
from user.test.helpers import clean_db, create_user, user_mock

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
client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_session():
    clean_db(engine)
    yield
    clean_db(engine)


@pytest.fixture(autouse=True)
def setup_and_teardown_each_test():
    clean_db(engine)
    yield
    clean_db(engine)


def test_singup():
    response = client.post("/signup", json=user_mock)
    assert response.status_code == 200
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user = session.query(UserSchema).filter_by(
            email=user_mock["email"]).first()

        assert user != None
        
        payload = verify_jwt(response.json()["token"])
        assert payload["username"] == user_mock["email"]
        
def test_singup_duplicate_email():
    response = client.post("/signup", json=user_mock)
    assert response.status_code == 200
    response = client.post("/signup", json=user_mock)
    assert response.status_code == 409
        

def test_login():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        create_user(session)
        response = client.post("/login", json=user_mock)
        assert response.status_code == 200
        payload = verify_jwt(response.json()["token"])
        assert payload["username"] == user_mock["email"]
        
def test_login_user_dosent_exist():
    response = client.post("/login", json=user_mock)
    assert response.status_code == 404
        