from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base
from settings import settings
url = URL.create(
    drivername="postgresql",
    username=settings.db_username,
    database=settings.db_database,
    password=settings.db_password,
    host=settings.db_host
)
print(url)
engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized the db")
