from fastapi import FastAPI

from database import create_db_and_tables
from notes_router import router as verify_router

app = FastAPI()

app.include_router(
    verify_router
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
