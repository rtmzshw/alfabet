from fastapi import APIRouter, Depends, FastAPI
from user.userTypes import UserCreationRequest, UserLoginRequest, JwtResponse
from user.userDal import add_user, get_user
from user.userUtils import create_jwt, hash_password
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from responses import not_found, unauthorized, conflict
app = FastAPI(root_path="/user")

@app.post("/signup", response_model=JwtResponse, responses={**conflict})
async def signup(user: UserCreationRequest):
    try:
        user.password = hash_password(user.password)
        new_user_id = add_user(user)
        jwt = create_jwt(new_user_id, user.email)

        return {"token": jwt}
    except IntegrityError:
        return JSONResponse(status_code=409, content={'detail': "email already exist", })
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'detail': "internal server error", })


@app.post("/login", response_model=JwtResponse, responses={**not_found})
async def login(user_login_request: UserLoginRequest):
    user_login_request.password = hash_password(user_login_request.password)
    user_id = get_user(user_login_request)

    if user_id == None:
        return JSONResponse(status_code=404, content={'detail': "user dosent exist", })

    jwt = create_jwt(user_id, user_login_request.email)
    return {"token": jwt}
