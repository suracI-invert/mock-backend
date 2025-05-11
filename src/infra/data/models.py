from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(BaseSchemaModel):
    id: int | None = None
    name: str
    email: str
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    email: str
    avatarUrl: str
    is_logged_in: bool


class Lesson(BaseSchemaModel):
    id: int | None = None
    name: str
    description: str
    type: str
    level: int
    content: dict[str, Any]
    authorId: int | None = None


class Document(BaseSchemaModel):
    id: int | None = None
    url: str
    lessonId: int | None = None


class Result(BaseSchemaModel):
    id: int | None = None
    score: int
    maxScore: int
    comment: str
    detail: dict[str, Any] | None = None
    startedAt: datetime
    endAt: datetime | None = None
    userId: int | None = None
    lessonId: int | None = None
