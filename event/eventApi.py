from fastapi import APIRouter, Depends
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from event.eventTypes import EventCreationRequest, EventUpdateRequest, QueryOptions, SortingOptions
from event.eventDal import add_event, get_event, delete_event, update_event, get_events as get_events_db
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from datetime import date as dateType
from typing import Annotated
from typing import List, Union
from fastapi import Query, Request
from utils import get_coordinates_from_geom

app = FastAPI(root_path="/event")

class Id(BaseModel):
    id: int

# TODO read about indexes for performance


@app.post("/", response_model=Id, responses={400: {"detail": "Event already exist"}, 500: {}})
async def create_event(event: EventCreationRequest, request: Request):
    try:
        print(request.state.user_id)
        event_id = add_event(event)
        return {"id": event_id}
    except IntegrityError as e:
        return JSONResponse(status_code=400, content={
            'detail': "Event already exist", })


@app.get("/{event_id}")
async def get_event_by_id(event_id: int):
    event = get_event(event_id)

    if event == None:
        raise HTTPException(status_code=404)

    event.location = get_coordinates_from_geom(event.location)
    return event

# TODO why i seperated the list https://github.com/tiangolo/fastapi/issues/2869
@app.get("/search")
async def get_events(query_options: QueryOptions = Depends(),
                     location: Annotated[Union[List[float],
                                               None], Query()] = None,
                     sorting_options: SortingOptions = Depends()):

    events = get_events_db(query_options, location, sorting_options)

    for event in events:
        event.location = get_coordinates_from_geom(event.location)

    return events


@app.delete("/{event_id}")
async def delete_event_by_id(event_id: int):
    is_deleted = delete_event(event_id)

    if not is_deleted:
        raise HTTPException(status_code=404)

    return {"ok": True}


@app.put("/{event_id}")
async def update_event_by_id(event_id: str, eventUpdateRequest: EventUpdateRequest):
    updateAsJson = jsonable_encoder(eventUpdateRequest)

    update_without_nones = {key: value for key,
                            value in updateAsJson.items() if value is not None}
    is_filter_empty = not bool(update_without_nones)

    if (is_filter_empty):
        raise HTTPException(status_code=400)

    is_updated = update_event(event_id, update_without_nones)

    if not is_updated:
        raise HTTPException(status_code=404)

    return {"ok": True}
