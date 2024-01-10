import uvicorn
from fastapi import FastAPI
from user.userApi import app as user_app
from postgrese import init_db
from middleweares import log_decorator, authenticate
from starlette.middleware.base import BaseHTTPMiddleware
from event.eventApi import app as event_app

app = FastAPI()
# TODO env
event_app.add_middleware(BaseHTTPMiddleware, dispatch=authenticate)
event_app.add_middleware(BaseHTTPMiddleware, dispatch=log_decorator)

user_app.add_middleware(BaseHTTPMiddleware, dispatch=log_decorator)

app.mount("/event",event_app)
app.mount("/",user_app)

if __name__ == "main":
    init_db()
