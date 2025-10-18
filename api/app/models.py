import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship, create_engine, Session


class Season(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    achievements: List["Achievement"] = Relationship(
        back_populates="season", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserAchievementLink(SQLModel, table=True):
    user_id: str = Field(
        foreign_key="user.id",
        primary_key=True,
    )
    achievement_id: str = Field(
        foreign_key="achievement.id",
        primary_key=True,
    )
    created_at: Optional[str] = Field(
        default_factory=lambda: datetime.datetime.now().isoformat(),
        nullable=False,
    )
    user: "User" = Relationship(
        back_populates="achievement_links", sa_relationship_kwargs={"lazy": "selectin"}
    )
    achievement: "Achievement" = Relationship(
        back_populates="user_links", sa_relationship_kwargs={"lazy": "selectin"}
    )


class Achievement(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    description: str
    emoji: str
    max_frequency_per_user: int = (1,)
    bounty: int = (0,)
    season_id: int = Field(foreign_key="season.id")

    season: Optional[Season] = Relationship(
        back_populates="achievements", sa_relationship_kwargs={"lazy": "selectin"}
    )
    user_links: List[UserAchievementLink] = Relationship(
        back_populates="achievement", sa_relationship_kwargs={"lazy": "selectin"}
    )


class User(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    name: str
    nick: Optional[str] = None
    discord_avatar_url: Optional[str] = None
    achievement_links: List[UserAchievementLink] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
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


def db_session():
    with Session(engine) as session:
        return session
