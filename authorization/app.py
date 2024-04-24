from fastapi import FastAPI

from database import create_db_and_tables
from schemas import UserRead, UserCreate, UserUpdate
from users import fastapi_users, auth_backend
from verify_handler import router as verify_router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/authorization/jwt",
    tags=["authorization"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/authorization",
    tags=["authorization"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/authorization",
    tags=["authorization"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/authorization",
    tags=["authorization"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    verify_router
)


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
