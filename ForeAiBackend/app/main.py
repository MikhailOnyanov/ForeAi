from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlmodel import Session, create_engine
from dotenv import load_dotenv

from .common import description
from .db import SQLModel, get_session, create_db_and_tables
from .routers import documentation, data, message, customer_service
from .dependencies import logger


create_db_and_tables()

app = FastAPI(
    title="ForeAiBackend",
    description=description,
    summary="API for managing ForeAi. "
            "Here you can find endpoints for managing Users, Companies, Subscriptions, AI models, Vector DB e.t.c.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mikhail Onyanov",
        "url": "https://t.me/michael_oni",
        "email": "mnonyanov@edu.hse.ru",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
)

app.include_router(documentation.router)
app.include_router(data.router)
app.include_router(message.router)
app.include_router(customer_service.router)

logger.info("Started FastAPI server")

@app.get("/")
async def root():
    return {"message": "Welcome to ForeAiBackend!"}
