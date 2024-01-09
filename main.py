import uvicorn
from fastapi import FastAPI, HTTPException
from event.eventSchema import create_events_table
from event.eventTypes import EventCreationRequest
from event.eventDal import add_event, get_event
from postgrese import conn
from psycopg2.errors import UniqueViolation
app = FastAPI()

create_events_table()


@app.post("/event")
async def create_event(event: EventCreationRequest):
    try:
        event_id = add_event(event)
        return {"id": event_id}
    except UniqueViolation:
        raise HTTPException(status_code=400, detail="Event already exist")
    except Exception:
        raise HTTPException(status_code=500)


@app.get("/event/{event_id}")
async def create_event(event_id: int):
    event = get_event(event_id)
    return event.toJson()


# uvicorn.run(app, host="0.0.0.0", port=8000)
