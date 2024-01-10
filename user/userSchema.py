from datetime import date as dateType
from pypika import Query, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index
from geoalchemy2 import Geometry
from datetime import datetime
from postgrese import Base

EVENT_TABLE = 'users'

class UserSchema(Base):
    __tablename__ = EVENT_TABLE
    id = Column(Integer(), primary_key=True)
    email = Column(String(100), nullable=False)
    password = Column(String(300), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)


Index('email', UserSchema.email, unique=True)
