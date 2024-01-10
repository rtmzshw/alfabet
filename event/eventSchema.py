from datetime import date as dateType
from pypika import Query, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index
from geoalchemy2 import Geometry
from datetime import datetime
from postgrese import Base

EVENT_TABLE = 'events'
class EventSchema(Base):
    __tablename__ = EVENT_TABLE
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    venue = Column(String(100), nullable=False)
    location = Column(Geometry('POINT'), nullable=False)
    date = Column(DateTime(), nullable=False)
    popularity = Column(Integer(), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)
    
Index('name_date_venue', EventSchema.name, EventSchema.date, EventSchema.venue, unique=True)