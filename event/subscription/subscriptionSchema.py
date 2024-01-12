from datetime import date as dateType
from pypika import Query, Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from postgrese import Base
from user.userSchema import USER_TABLE
from event.eventSchema import EVENT_TABLE

SUBSCRIPTION_TABLE = 'subscription'


class SubscriptionSchema(Base):
    __tablename__ = SUBSCRIPTION_TABLE
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey(f"{USER_TABLE}.id"))
    event_id = Column(Integer, ForeignKey(f"{EVENT_TABLE}.id"))
    creation_date = Column(DateTime(), nullable=False, default=datetime.now)


Index('user_id_event_id', SubscriptionSchema.user_id,
      SubscriptionSchema.event_id, unique=True)
