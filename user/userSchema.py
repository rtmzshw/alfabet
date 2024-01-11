from datetime import date as dateType
from pypika import Query, Column
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Index
from geoalchemy2 import Geometry
from datetime import datetime
from postgrese import Base

USER_TABLE = 'users'
class UserSchema(Base):
    __tablename__ = USER_TABLE
    id = Column(Integer(), primary_key=True)
    email = Column(String(100), nullable=False,)
    password = Column(String(300), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)
    # events = relationship('EventSchema', back_populates='user')


Index('email', UserSchema.email, unique=True)
