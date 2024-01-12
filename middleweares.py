import time

from fastapi import Request, HTTPException, Response
from logger.logger import log_info, log_error
from user.userUtils import verify_jwt
from fastapi.responses import JSONResponse

async def log_decorator(request: Request, call_next):
    try:
        start_time = time.time()
        log_info("started handeling", {
                 "url": request.url})
        response:Response = await call_next(request)
    except Exception as e:
        process_time = time.time() - start_time
        log_error(e, "failed handeling", {
                  "url": request.url, "process_time": process_time})
        return JSONResponse(status_code=500, content="Internal server error")

    process_time = time.time() - start_time
    log_info("success handeling", {
             "url": request.url, "process_time": process_time,
             "status": response.status_code})
    return response


async def authenticate(request: Request, call_next):
    
    # Skip the middleware logic for docs
    if("openapi.json" in request.url.path or "docs" in request.url.path):
        return await call_next(request)
    
    if(not "Authorization" in request.headers):
        return JSONResponse(status_code=401, content="No authorization token")
    
    token = request.headers["Authorization"]
    if (not token):
        return JSONResponse(status_code=401, content="Empty authorization token")
    
    payload = verify_jwt(token)
    if(not payload):
        return JSONResponse(status_code=401, content="Bad authorization token")
    
    request.state.user_id = payload["user_id"]
    response = await call_next(request)
    return response
