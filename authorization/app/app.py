from fastapi import FastAPI

from database import create_db_and_tables
from schemas import UserRead, UserCreate, UserUpdate
from user_router import router as user_router
from users import fastapi_users, auth_backend
from verify_router import router as verify_router

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

app.include_router(
    user_router
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
