import uvicorn
from fastapi import FastAPI
from user.userApi import app as user_app
from postgrese import init_db
from middleweares import log_decorator, authenticate
from starlette.middleware.base import BaseHTTPMiddleware
from event.eventApi import app as event_app
from utils import set_interval
from notification.notificationLogic import register_notifications
app = FastAPI()
    
# event_app.add_middleware(BaseHTTPMiddleware, dispatch=authenticate)
event_app.add_middleware(BaseHTTPMiddleware, dispatch=log_decorator)
user_app.add_middleware(BaseHTTPMiddleware, dispatch=log_decorator)
app.mount("/event",event_app)
app.mount("/user",user_app)

register_notifications()

if __name__ == "main":
    init_db()
