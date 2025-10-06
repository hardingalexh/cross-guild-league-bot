from fastapi import FastAPI
from app import models

models.create_db_and_tables()
app = FastAPI()


@app.on_event("startup")
def on_startup():
    models.create_db_and_tables()


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
