from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from database import AccessToken, get_access_token_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization/jwt/login")


@router.get("/verify/token", tags=["token"])
async def is_verified_token(token: str = Depends(oauth2_scheme),
                            access_token_db: AccessToken = Depends(get_access_token_db)) -> str:
    stored_token = await access_token_db.get_by_token(token)
    if not stored_token:
        raise HTTPException(status_code=404, detail="Token not found")

    if stored_token.token != token:
        raise HTTPException(status_code=401, detail="Tokens do not match")

    return str(stored_token.user_id)
