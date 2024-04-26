from datetime import datetime
from datetime import timedelta
from typing import List, Optional

import httpx
from fastapi import APIRouter
from fastapi import Query, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from config import AUTH_MICROSERVICE_URL
from database import Note, get_async_session
from internet import get_author_id_from_token
from mapper import mapper_note_to_noteread, mapper_node_to_note_unauthorized
from schemas import NoteCreate, NoteUpdate, NoteRead, NoteReadUnauthorized
from schemas import NoteResponse
from service import get_data, get_notes, validate_date_parameters

router = APIRouter()

hard_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

soft_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


@router.post("/auth/login")
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


@router.post("/notes", response_model=NoteResponse)
async def create_note(note: NoteCreate,
                      token: str = Depends(hard_oauth2_scheme),
                      session: AsyncSession = Depends(get_async_session)):
    author_id = await get_author_id_from_token(token)
    db_note = Note(**note.dict(), author_id=author_id)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int,
                      note: NoteUpdate,
                      token: str = Depends(hard_oauth2_scheme),
                      session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Note).where(Note.note_id == note_id))
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    author_id = await get_author_id_from_token(token)
    if db_note.author_id != author_id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this note")
    one_day_ago = datetime.utcnow() - timedelta(hours=24)
    if db_note.creation_date < one_day_ago:
        raise HTTPException(status_code=403, detail="You can only edit notes created within the last 24 hours")
    for key, value in note.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@router.get("/notes", response_model=List[NoteRead | NoteReadUnauthorized])
async def read_notes_feed(
        token: str = Depends(soft_oauth2_scheme),
        session: AsyncSession = Depends(get_async_session),
        limit: int = Query(1, ge=1, description="Page number"),
        offset: int = Query(10, ge=1, le=100, description="Number of notes per page"),
        from_date: Optional[str] = Query(None, description="Filter notes from this date (ISO format)"),
        to_date: Optional[str] = Query(None, description="Filter notes to this date (ISO format)"),
        author_id: Optional[str] = Query(None, description="Filter notes by author_id"),
):
    current_user_id = await get_author_id_from_token(token) if token else None

    from_date_obj = await get_data(from_date)
    to_date_obj = await get_data(to_date)

    await validate_date_parameters(from_date_obj, to_date_obj)

    notes = await get_notes(author_id, from_date_obj, limit, offset, session, to_date_obj)

    note_read_list: List[NoteRead | NoteReadUnauthorized] = []
    for note in notes:
        if current_user_id:
            note_read = await mapper_note_to_noteread(current_user_id, note)
        else:
            note_read = await mapper_node_to_note_unauthorized(note)
        note_read_list.append(note_read)

    return note_read_list
