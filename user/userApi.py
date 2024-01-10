from fastapi import APIRouter, Depends, FastAPI
from user.userTypes import UserCreationRequest, UserLoginRequest
from user.userDal import add_user, get_user
from user.userUtils import create_jwt, hash_password
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

app = FastAPI(root_path="/")

# TODO logging


@app.post("/signup")
async def signup(user: UserCreationRequest):
    try:
        user.password = hash_password(user.password)
        new_user_id = add_user(user)
        jwt = create_jwt(new_user_id, user.email)

        return {"token": jwt}
    except IntegrityError:
        return JSONResponse(status_code=400, content={'detail': "email already exist", })
    except Exception:
        return JSONResponse(status_code=500)


@app.post("/login")
async def get_event_by_id(user_login_request: UserLoginRequest):
    user_login_request.password = hash_password(user_login_request.password)
    user_id = get_user(user_login_request)
    
    if user_id == None:
        return JSONResponse(status_code=404, content={'detail': "user dosent exist", })

    jwt = create_jwt(user_id, user_login_request.email)
    return jwt
