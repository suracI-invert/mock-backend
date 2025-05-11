from typing import Annotated

import httpx
import jwt
from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

from settings import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/v1/token")

router = APIRouter(prefix="/auth/v1", tags=["user"])


@router.get("/login")
async def login(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings.auth.client_id}&redirect_uri={settings.auth.redirect_uri.unicode_string()}&scope=openid%20profile%20email&access_type=offline"
    }


@router.get("/access")
async def access_token(code: str, settings: Annotated[Settings, Depends(get_settings)]):
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": settings.auth.client_id,
        "client_secret": settings.auth.client_secret.get_secret_value(),
        "redirect_uri": settings.auth.redirect_uri.unicode_string(),
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(token_url, data=data)
        access_token = response.json().get("access_token")
        user_info = await client.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
    return user_info.json()


@router.get("/token")
async def get_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    return jwt.decode(
        token, settings.auth.client_secret.get_secret_value(), algorithms=["HS256"]
    )
