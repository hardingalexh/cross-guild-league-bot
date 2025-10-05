from fastapi import FastAPI
from pydantic import BaseModel
from app import models

models.create_db_and_tables()

app = FastAPI()


class Hello(BaseModel):
    message: str


@app.get("/", response_model=Hello)
async def hello() -> Hello:
    print("hey")
    return Hello(message="Hi, I am using FastAPI")
