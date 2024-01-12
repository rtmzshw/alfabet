import time
import jwt
import os
from user.userConfig import jwt_ttl, jwt_algorithem, jwt_secret_key, hash_salt
import bcrypt
from user.userTypes import JwtPayload


def create_jwt(user_id: int, user_email: str):
    experation_time = time.time() + jwt_ttl

    payload: JwtPayload = {
        'user_id': str(user_id),
        'username': user_email,
        'exp': experation_time
    }

    token = jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithem)
    return token


def verify_jwt(token: str):
    try:
        payload: JwtPayload = jwt.decode(
            token, jwt_secret_key, algorithms=[jwt_algorithem])
        return payload
    except jwt.ExpiredSignatureError as e:
        return False
    except jwt.InvalidTokenError as e:
        return False


def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), hash_salt).decode()
