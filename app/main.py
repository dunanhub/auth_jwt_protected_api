from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import router as user_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(user_router)