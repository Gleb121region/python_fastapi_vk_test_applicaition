from fastapi import APIRouter, Depends, HTTPException

from database import AccessToken, get_access_token_db

router = APIRouter()


@router.get("/verify/token", tags=["token"])
async def is_verified_token(token: str, access_token_db: AccessToken = Depends(get_access_token_db)) -> str:
    stored_token = await access_token_db.get_by_token(token)
    if not stored_token:
        raise HTTPException(status_code=404, detail="Token not found")

    if stored_token.token != token:
        raise HTTPException(status_code=401, detail="Tokens do not match")

    return str(stored_token.user_id)
