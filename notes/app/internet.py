import httpx
from fastapi import HTTPException

from config import AUTH_MICROSERVICE_URL


async def get_author_id_from_token(token: str) -> str:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_MICROSERVICE_URL}/verify/token", headers=headers)
        if response.status_code == 200:
            return response.text.replace("\"", "")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)


async def get_author_login_by_id(author_id: str) -> str:
    headers = {
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{AUTH_MICROSERVICE_URL}/users/{author_id}/email", headers=headers)
        if response.status_code == 200:
            return response.text.replace("\"", "")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
