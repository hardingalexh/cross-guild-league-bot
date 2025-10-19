from fastapi import FastAPI, HTTPException
from app import models
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os

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
    nick: Optional[str] = None
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
            db_user.discord_avatar_url = user.discord_avatar_url
        else:
            db_user = models.User(
                id=user.id,
                name=user.name,
                nick=user.nick,
                discord_avatar_url=user.discord_avatar_url,
            )
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
        if db_achievement.id not in [
            al.achievement_id for al in db_user.achievement_links
        ]:
            db_user.achievement_links.append(
                models.UserAchievementLink(
                    achievement_id=db_achievement.id, user_id=db_user.id
                )
            )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user


@app.post("/user/remove_achievement", response_model=models.User)
async def remove_achievement_to_user(user: models.User, emoji: str) -> models.User:
    """Removes an achievement from a user.

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
        if db_achievement.id in [al.achievement_id for al in db_user.achievement_links]:
            link = next(
                (
                    al
                    for al in db_user.achievement_links
                    if al.achievement_id == db_achievement.id
                ),
                None,
            )
            if link:
                db_user.achievement_links.remove(link)
                session.delete(link)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
        return db_user


@app.get("/achievements", response_model=List[models.Achievement])
async def get_achievements(season: int = None) -> List[models.Achievement]:
    """Gets achievements for the latest season by default, or for a given season."""
    with models.db_session() as session:
        if season is None:
            latest_season = (
                session.query(models.Season).order_by(models.Season.id.desc()).first()
            )
            if not latest_season:
                return []
            season_id = latest_season.id
        else:
            season_id = season
        achievements = (
            session.query(models.Achievement).filter_by(season_id=season_id).all()
        )
        return achievements


@app.get("/seasons", response_model=List[models.Season])
async def get_seasons() -> List[models.Season]:
    """Gets all seasons."""
    with models.db_session() as session:
        seasons = session.query(models.Season).order_by(models.Season.id.desc()).all()
        return seasons


@app.get("/leaderboard", response_model=List[UserResponse])
async def get_leaderboard(season: int = None) -> List[UserResponse]:
    """Gets a leaderboard: list of users with their achievement_links for a season.
    Defaults to the latest season when no season id is provided.
    """
    with models.db_session() as session:
        if season is None:
            latest_season = (
                session.query(models.Season).order_by(models.Season.id.desc()).first()
            )
            if not latest_season:
                return []
            season_id = latest_season.id
        else:
            season_id = season

        # Get users who have at least one achievement in the requested season
        users = (
            session.query(models.User)
            .join(models.UserAchievementLink)
            .join(models.Achievement)
            .filter(models.Achievement.season_id == season_id)
            .distinct()
            .all()
        )

        # Filter each user's achievement_links to only include links for the requested season
        for u in users:
            u.achievement_links = [
                al
                for al in u.achievement_links
                if al.achievement.season_id == season_id
            ]

        return users
