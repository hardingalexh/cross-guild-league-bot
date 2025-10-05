from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


class Season(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    achievements: List["Achievement"] = Relationship(back_populates="season")


class UserAchievementLink(SQLModel, table=True):
    user_id: int = Field(
        foreign_key="user.id",
        primary_key=True,
    )
    achievement_id: int = Field(
        foreign_key="achievement.id",
        primary_key=True,
    )


class Achievement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    emoji: str
    season_id: int = Field(foreign_key="season.id")

    season: Optional[Season] = Relationship(back_populates="achievements")
    users: List["User"] = Relationship(
        back_populates="achievements", link_model=UserAchievementLink
    )


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    discord_id: str

    achievements: List["Achievement"] = Relationship(
        back_populates="users", link_model=UserAchievementLink
    )


# Database connection
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "example"
POSTGRES_NAME = "postgres"
POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    newUser = User(name="ExampleUser", discord_id="123456789")
    newSeason = Season(name="Spring 2024")
    newAchievement = Achievement(name="First Win", emoji="🏆", season=newSeason)
    newUser.achievements.append(newAchievement)


# Usage example:
# create_db_and_tables()
