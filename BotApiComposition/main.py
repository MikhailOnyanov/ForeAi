from fastapi import Depends, FastAPI

from .routers import telegram

app = FastAPI()

app.include_router(
    telegram.router,
    prefix="/telegram",
    tags=["telegram"],
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}