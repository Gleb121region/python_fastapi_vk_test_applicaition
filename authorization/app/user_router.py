from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import User, get_async_session

router = APIRouter()


async def get_user_email(user_id: str, session: AsyncSession) -> str:
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user:
        return user.email
    else:
        raise ValueError(f"User with ID {user_id} not found")


@router.get("/users/{user_id}/email", tags=["users"])
async def get_email(user_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        return await get_user_email(user_id, session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
