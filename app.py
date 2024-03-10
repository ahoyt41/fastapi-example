from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


class Request(BaseModel):
    x: int
    y: int


class Response(BaseModel):
    result: Optional[int] = None
    error: Optional[str] = None


app = FastAPI()


@app.get("/add")
def add(request: Request) -> Response:
    return Response(result=request.x + request.y)
