from fastapi import FastAPI

from .routers import documentation, data, message

app = FastAPI()

app.include_router(documentation.router)
app.include_router(data.router)
app.include_router(message.router)


@app.get("/")
async def root():
    return {"message": "Welcome to ForeAiBackend!"}
