import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine
from .models import user
from .dependencies import logger


# Loading .env parameters

db_uri = os.getenv("DATABASE_CONNECTION_STRING", "postgresql://admin:admin@127.0.0.1:5433/foreaidb")

logger.info(f"Connecting to DB with uri: {db_uri}")
engine = create_engine(db_uri)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]