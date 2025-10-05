import uuid
from typing import List, Optional
from pydantic import BaseModel


class SeasonSchema(BaseModel):
    id: uuid.UUID
    name: str
    achievements: Optional[List["AchievementSchema"]] = []

    class Config:
        orm_mode = True


class AchievementSchema(BaseModel):
    id: uuid.UUID
    name: str
    react: str
    bounty: str
    frequency: str
    seasons: Optional[List[SeasonSchema]] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: uuid.UUID
    discord_id: str
    name: str
    achievements: Optional[List[AchievementSchema]] = []

    class Config:
        orm_mode = True


# For circular references in Pydantic
SeasonSchema.update_forward_refs()
AchievementSchema.update_forward_refs()
UserSchema.update_forward_refs()
