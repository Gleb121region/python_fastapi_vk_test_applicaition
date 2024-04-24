import logging

import httpx
from fastapi import Depends
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from config import AUTH_MICROSERVICE_URL, NOTES_MICROSERVICE_URL
from schemas import *

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@app.post("/auth/login")
async def route_to_login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    data = {
        "grant_type": form_data.grant_type,
        "username": form_data.username,
        "password": form_data.password,
        "scope": form_data.scopes,
        "client_id": form_data.client_id,
        "client_secret": form_data.client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/jwt/login", data=data,
                                     headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/auth/register")
async def route_to_register_user(dto: UserRegistration):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/register", json=dto.dict())
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/auth/forgot-password")
async def route_to_forgot_password_user(dto: UserForgotPassword):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/forgot-password", json=dto.dict())
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/auth/reset-password")
async def route_to_reset_password_user(dto: UserResetPassword):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/reset-password", json=dto.dict())
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/auth/request-verify-token")
async def route_to_request_verify_token_user(dto: UserRequestVerifyToken):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/request-verify-token", json=dto.dict())
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/auth/verify")
async def route_to_request_verify(dto: UserVerifyToken):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_MICROSERVICE_URL}/authorization/verify", json=dto.dict())
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/current-user")
async def route_to_get_info_about_current_user(token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_MICROSERVICE_URL}/users/me", headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.patch("/update/me")
async def route_to_patch_info_about_current_user(dto: UserPatch, token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{AUTH_MICROSERVICE_URL}/users/me", json=dto.dict(), headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/user/{uuid}")
async def route_to_get_info_about_other_user_by_id(uuid: str, token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_MICROSERVICE_URL}/users/{uuid}", headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/notes/")
async def create_note(note: NoteCreate, token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{NOTES_MICROSERVICE_URL}/notes/", json=note.dict(), headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.put("/notes/{note_id}")
async def update_note(note_id: int, note: NoteUpdate, token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{NOTES_MICROSERVICE_URL}/notes/{note_id}", json=note.dict(), headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())


@app.get("/notes/")
async def read_notes(skip: int = 0, limit: int = 100, token: str = Depends(oauth2_scheme)):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NOTES_MICROSERVICE_URL}/notes/", params={"skip": skip, "limit": limit},
                                    headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())
