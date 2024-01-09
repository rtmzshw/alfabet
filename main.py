from fastapi import FastAPI
from event.eventSchema import EventCreationRequest,create_events_table
from event.eventDal import add_event
from postgrese import conn
app = FastAPI()

create_events_table()

@app.post("/event")
async def create_event(event: EventCreationRequest):
    try:
        print("hi")
        add_event(event)
    except Exception as e:
        print(e)
        return e
        
    return {"message": "Hello World"}

@app.get("/")
async def create_event():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE event_id = 1")
    res = cursor.fetchone()
    return {"message": res}