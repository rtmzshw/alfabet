from user.userSchema import UserSchema
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from user.userUtils import hash_password

user_mock = {"email": "rtmzshw@gmail.com", "password": "12345678"}

def clean_db(engine: Engine):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        session.query(UserSchema).delete()
        session.commit()


def create_user(session: Session, email: str = user_mock["email"], password: str = user_mock["password"]):
    new_user = UserSchema(
        email=email, password=hash_password(password))
    session.add(new_user)
    session.commit()
    return new_user
