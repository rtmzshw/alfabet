import time
import jwt
import os
from user.userConfig import jwt_ttl, jwt_algorithem, JWT_SECRET_KEY, hash_salt
import bcrypt
def create_jwt(user_id: int, user_email: str):
    experation_time = time.time() + jwt_ttl
    payload = {
        'user_id': str(user_id),
        'username': user_email,
        'exp': experation_time
    }
    
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=jwt_algorithem)
    return token

def verify_jwt(token:str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[jwt_algorithem])
        return payload
    except jwt.ExpiredSignatureError as e:
        print(e)
        return False
    except jwt.InvalidTokenError as e:
        print(e)
        return False

def hash_password(password:str):
    return bcrypt.hashpw(password.encode('utf-8'), hash_salt).decode()
