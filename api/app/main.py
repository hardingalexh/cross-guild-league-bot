from fastapi import FastAPI, HTTPException
from app import models
from pydantic import BaseModel
from typing import List
from datetime import datetime

models.create_db_and_tables()
app = FastAPI()


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()


class AchievementLinkResponse(BaseModel):
    achievement_id: str
    created_at: datetime
    achievement: models.Achievement


class UserResponse(BaseModel):
    id: str
    name: str
    nick: str
    achievement_links: List[AchievementLinkResponse]

    class Config:
        orm_mode = True


@app.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: str) -> UserResponse:
    """Gets a user by ID, including achievements with created_at datestamp."""
    with models.db_session() as session:
        db_user = session.query(models.User).filter_by(id=user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.post("/user/upsert", response_model=models.User)
async def upsert_user(user: models.User) -> models.User:
    """Upserts a user into the database.

    Args:
        user (models.User): The user to upsert, from discord.

    Returns:
        models.User: The refreshed user from the database.
    """
    with models.db_session() as session:
        db_user = session.get(models.User, user.id)
        if db_user:
            db_user.name = user.name
            db_user.nick = user.nick
        else:
            db_user = models.User(id=user.id, name=user.name, nick=user.nick)
            session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.post("/user/add_achievement", response_model=models.User)
async def add_achievement_to_user(user: models.User, emoji: str) -> models.User:
    """Adds an achievement to a user.

    Args:
        user (User): A user.
        achievement (achievement): An achievement.
    """
    with models.db_session() as session:
        db_user = session.query(models.User).filter_by(id=user.id).first()
        db_achievement = (
            session.query(models.Achievement).filter_by(emoji=emoji).first()
        )
        if not db_user or not db_achievement:
            raise HTTPException(status_code=404, detail="User or Achievement not found")
        if db_achievement not in db_user.achievements:
            db_user.achievements.append(db_achievement)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user


@app.post("/user/remove_achievement", response_model=models.User)
async def remove_achievement_from_user(user: models.User, emoji: str) -> models.User:
    """Removes an achievement from a user.

    Args:
        user (User): A user.
        emoji (str): The emoji representing the achievement.
    """
    with models.db_session() as session:
        db_user = session.get(models.User, user.id)
        db_achievement = (
            session.query(models.Achievement).filter_by(emoji=emoji).first()
        )
        if not db_user or not db_achievement:
            raise HTTPException(status_code=404, detail="User or Achievement not found")
        if db_achievement in db_user.achievements:
            db_user.achievements.remove(db_achievement)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user
