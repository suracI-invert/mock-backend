from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from infra.data.crud import DataBackend
from infra.data.models import User

from ..dependencies.resources import get_data_backend
from ..models.user import CreateUser, UpdateUser

router = APIRouter(prefix="/user/v1", tags=["user"])


@router.get("/{email}")
async def me(
    email: str, data_backend: Annotated[DataBackend, Depends(get_data_backend)]
):
    result = await data_backend.get_user_by_email(email=email)
    if not result:
        raise HTTPException(404, "User not found")
    return result


@router.post("/create")
async def create_user(
    user: CreateUser, data_backend: Annotated[DataBackend, Depends(get_data_backend)]
):
    result = await data_backend.create_user(User.model_validate(user))
    return result


@router.post("/update")
async def update_user(
    user: UpdateUser, data_backend: Annotated[DataBackend, Depends(get_data_backend)]
):
    result = await data_backend.update_user(User.model_validate(user))
    return result
