from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Hello(BaseModel):
    message: str


@app.get("/", response_model=Hello)
async def hello() -> Hello:
    return Hello(message="Hi, I am using FastAPI")
