from datetime import date as dateType
from pypika import Query, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from postgrese import Base
from event.eventSchema import EVENT_TABLE
NOTIFICATION_TABLE = 'notifications'


class NotificationSchema(Base):
    __tablename__ = NOTIFICATION_TABLE
    id = Column(Integer(), primary_key=True)
    description = Column(String(), nullable=True)
    date = Column(DateTime(), nullable=False)
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)
    sent = Column(Boolean(), nullable=False, default=False)
    event_id = Column(Integer, ForeignKey(f"{EVENT_TABLE}.id"))
