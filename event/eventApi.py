from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from event.eventTypes import EventCreationRequest, EventUpdateRequest, QueryOptions, SortingOptions, Id, Event, Ok, SubscriptionStatus
from event.eventDal import add_event, get_event, delete_event, update_event, get_events as get_events_db
from event.subscription.subscriptionDal import toggle_subscription
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import date as dateType
from typing import Annotated
from typing import List, Union
from fastapi import Query, Request
from utils import get_coordinates_from_geom
from errors import Unauthorized, NotFound
from responses import not_found, unauthorized, conflict
app = FastAPI(root_path="/event")


# seperated location from query option because its impossible to put a list in a class
# https://github.com/tiangolo/fastapi/issues/2869
@app.get("/search", response_model=List[Event])
async def get_events(query_options: QueryOptions = Depends(),
                     location: Annotated[Union[List[float],
                                               None], Query()] = None,
                     sorting_options: SortingOptions = Depends()):

    events = get_events_db(query_options, location, sorting_options)

    for event in events:
        event.location = get_coordinates_from_geom(event.location)

    return events


@app.post("/", response_model=Id, responses={**conflict})
async def create_event(event: EventCreationRequest, request: Request):
    try:
        event_id = add_event(event, request.state.user_id)
        return {"id": event_id}
    except IntegrityError as e:
        print(e)
        return JSONResponse(status_code=409, content={
            'detail': "Event already exist", })


@app.get("/{event_id}", response_model=Event, responses={**not_found})
async def get_event_by_id(event_id: int):
    event = get_event(event_id)

    if event == None:
        return JSONResponse(status_code=404, content={'detail': "Not found", })

    event.location = get_coordinates_from_geom(event.location)
    return event


@app.delete("/{event_id}", response_model=Ok, responses={**not_found, **unauthorized})
async def delete_event_by_id(event_id: int, request: Request):
    try:
        delete_event(event_id, request.state.user_id)
    except Unauthorized:
        return JSONResponse(status_code=401, content={'detail': "Unautorized", })
    except NotFound:
        return JSONResponse(status_code=404, content={'detail': "Not found", })

    return {"ok": True}


@app.put("/{event_id}", response_model=Ok, responses={**not_found, **unauthorized, 400: {'detail': "Update cant be empty"}})
async def update_event_by_id(event_id: str, eventUpdateRequest: EventUpdateRequest, request: Request):
    try:
        updateAsJson = jsonable_encoder(eventUpdateRequest)

        update_without_nones = {key: value for key,
                                value in updateAsJson.items() if value is not None}
        is_filter_empty = not bool(update_without_nones)

        if (is_filter_empty):
            raise HTTPException(status_code=400)
        
        update_event(event_id, update_without_nones, request.state.user_id)
    except Unauthorized:
        raise HTTPException(status_code=401)
    except NotFound:
        raise HTTPException(status_code=404)

    return {"ok": True}


@app.post("/subscription/toggle/{event_id}", response_model=SubscriptionStatus, responses={**not_found})
async def subscription(event_id, request: Request):
    try:
        status = toggle_subscription(request.state.user_id,event_id)
        return {"status": status}
    # event who dosent exist
    except IntegrityError as e:
        print(e)
        return JSONResponse(status_code=404, content={
            'detail': "event dosent exist", })
