from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Note, get_async_session
from schemas import NoteResponse, NoteCreate, NoteUpdate

router = APIRouter()


@router.get("/")
async def print_hello_world():
    return "Hello World"


@router.post("/notes/", response_model=NoteResponse)
async def create_note(note: NoteCreate, session: AsyncSession = Depends(get_async_session)):
    db_note = Note(**note.dict())
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@router.get("/notes/{note_id}", response_model=NoteResponse)
async def read_note(note_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Note).where(Note.note_id == note_id))
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note


@router.put("/notes/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteUpdate, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Note).where(Note.note_id == note_id))
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    await session.commit()
    await session.refresh(db_note)
    return db_note


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Note).where(Note.note_id == note_id))
    db_note = result.scalar_one_or_none()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await session.delete(db_note)
    await session.commit()
    return None
