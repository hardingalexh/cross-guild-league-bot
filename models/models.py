import uuid
from datetime import datetime

from sqlalchemy import Column, String, Table, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()

# Association table for Achievement <-> Season (many-to-many)
achievement_season = Table(
    "achievement_season",
    Base.metadata,
    Column(
        "achievement_id",
        UUID(as_uuid=True),
        ForeignKey("achievement.id"),
        primary_key=True,
    ),
    Column("season_id", UUID(as_uuid=True), ForeignKey("season.id"), primary_key=True),
)

# Association table for User <-> Achievement with date stamp (many-to-many)
user_achievement = Table(
    "user_achievement",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column(
        "achievement_id",
        UUID(as_uuid=True),
        ForeignKey("achievement.id"),
        primary_key=True,
    ),
    Column("date", DateTime, default=datetime.utcnow, nullable=False),
)


class Season(Base):
    __tablename__ = "season"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    achievements = relationship(
        "Achievement", secondary=achievement_season, back_populates="seasons"
    )


class Achievement(Base):
    __tablename__ = "achievement"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    react = Column(String, nullable=False)
    bounty = Column(String, nullable=False)
    frequency = Column(String, nullable=False)
    seasons = relationship(
        "Season", secondary=achievement_season, back_populates="achievements"
    )
    users = relationship(
        "User", secondary=user_achievement, back_populates="achievements"
    )


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    discord_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    achievements = relationship(
        "Achievement", secondary=user_achievement, back_populates="users"
    )


# Pydantic Schemas
