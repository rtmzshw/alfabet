from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

url = URL.create(
    drivername="postgresql",
    username="postgres",
    database="postgres",
    password="alfabet"
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Initialized the db")