from pypika import Query, Table, Schema
from event.eventSchema import EventSchema
from event.eventTypes import Event, EventCreationRequest, EventUpdateRequest, SortingOptions, QueryOptions
from postgrese import engine
from sqlalchemy.orm import sessionmaker
from utils import convert_to_point
from user.userTypes import User, UserLoginRequest
from user.userSchema import UserSchema


def add_user(user: User):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_user = UserSchema(email=user.email,
                                password=user.password
                              )
        session.add(new_user)
        session.commit()
        return new_user.id


def get_user(user_login_request: UserLoginRequest):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        user = session.query(UserSchema).filter_by(
            email=user_login_request.email, password=user_login_request.password).first()
        if (not user):
            return None
        
        return user.id
