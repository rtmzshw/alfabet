from fastapi import Request, HTTPException


def authenticateMock(id: str):
    async def middleware(request: Request, call_next):
        request.state.user_id = id
        response = await call_next(request)
        return response
    return middleware


event_mock = {"name": "rotem",
              "venue": "kikar55222",
              "date": "2024-01-11T10:45:00+02:00",
              "popularity": 200,
              "location": [5, 45]}
