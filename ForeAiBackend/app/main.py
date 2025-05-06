from fastapi import FastAPI

from .db import SQLModel, get_session, create_db_and_tables
from .routers import documentation, data, message, customer_service
import logging
from contextlib import asynccontextmanager
from .constants import chroma_service_config
from .dependencies import initialize_vector_db

logger = logging.getLogger(__name__)

# create_db_and_tables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load ChromaDB
    logger.info("INITIALIZING LIFESPAN")
    app.state.vector_db = initialize_vector_db("chroma", chroma_service_config)
    yield
    # After app shutdown

app = FastAPI(
    title="ForeAiBackend",
    description="ForeAI API helps you do awesome stuff. 🚀",
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
    lifespan=lifespan,
)

app.include_router(documentation.router)
app.include_router(data.router)
app.include_router(message.router)
app.include_router(customer_service.router)

logger.info("Started FastAPI server")

@app.get("/")
async def root():
    return {"message": "Welcome to ForeAiBackend!"}
