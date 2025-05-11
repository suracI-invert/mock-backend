from datetime import datetime
from typing import Any

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from ..db.postgre import Base


class IdentifiedMixin(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin(Base):
    __abstract__ = True

    createdAt: Mapped[datetime] = mapped_column(insert_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(
        insert_default=func.now(), onupdate=func.now()
    )


class User(IdentifiedMixin, TimestampMixin):
    __tablename__ = "users"

    name: Mapped[str]
    email: Mapped[str]
    avatarUrl: Mapped[str]
    is_logged_in: Mapped[bool]


class Lesson(IdentifiedMixin, TimestampMixin):
    __tablename__ = "lessons"

    name: Mapped[str]
    description: Mapped[str]
    type: Mapped[str]
    level: Mapped[int]
    content: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)

    authorId: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)


class Document(IdentifiedMixin, TimestampMixin):
    __tablename__ = "documents"

    url: Mapped[str] = mapped_column(nullable=False)

    lessonId: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)


class Result(IdentifiedMixin, TimestampMixin):
    __tablename__ = "results"

    score: Mapped[int]
    maxScore: Mapped[int]
    comment: Mapped[str]
    detail: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    startedAt: Mapped[datetime]
    endAt: Mapped[datetime | None] = mapped_column(nullable=True)

    userId: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lessonId: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)
