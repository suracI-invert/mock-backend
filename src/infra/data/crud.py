import logfire
from structlog.stdlib import BoundLogger
from sqlalchemy import select, update

from log import get_logger

from .models import User, Lesson, Document, Result
from .schema import (
    User as UserSchema,
    Lesson as LessonSchema,
    Document as DocumentSchema,
    Result as ResultSchema,
)

from ..db.postgre import PostgresClient


class DataBackend:

    def __init__(
        self,
        client: PostgresClient,
        logger: BoundLogger = get_logger("user_backend.postgres.backend"),
    ):
        self._client = client
        self._logger = logger

    @logfire.instrument("create_user")
    async def create_user(self, user: User) -> User:
        async with self._client.get_session() as session:
            try:
                obj = UserSchema(**user.model_dump(exclude_none=True))
                session.add(obj)
                await session.flush()
                await session.commit()
                await session.refresh(obj)
                await self._logger.ainfo("User created", user=user)
                return User.model_validate(obj)
            except Exception:
                await self._logger.aexception("Failed to create user", user=user)
                raise

    @logfire.instrument("get_user_by_email")
    async def get_user_by_email(self, email: str) -> User | None:
        async with self._client.get_session() as session:
            try:
                result = (
                    await session.execute(
                        select(UserSchema).where(UserSchema.email == email)
                    )
                ).scalar_one_or_none()
                if not result:
                    return None
                return User.model_validate(result)
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch user by email", email=email
                )
                raise

    @logfire.instrument("get_user_by_id")
    async def get_user_by_id(self, user_id: int):
        async with self._client.get_session() as session:
            try:
                result = await session.get(UserSchema, user_id)
                if not result:
                    return None
                return User.model_validate(result)
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch user by id", user_id=user_id
                )
                raise

    @logfire.instrument("update_user")
    async def update_user(self, user: User) -> User | None:
        async with self._client.get_session() as session:
            session.begin()
            try:
                assert user.id
                stmt = (
                    update(UserSchema)
                    .where(UserSchema.id == user.id)
                    .values(**user.model_dump(exclude_none=True, exclude={"id"}))
                    .returning(UserSchema)
                )

                await self._logger.ainfo("User updated SQL", stmt=str(stmt))
                result = (await session.execute(stmt)).scalar_one_or_none()
                if not result:
                    await self._logger.aexception("Found no user", user=user)
                    return None
                new_user = User.model_validate(result)
            except Exception:
                await session.rollback()
                await self._logger.aexception("Failed to update user", user=user)
                raise
            else:
                await session.commit()
                await self._logger.ainfo("User updated", user=user)
                return new_user

    @logfire.instrument("delete_user")
    async def delete_user(self, user_id: int):
        async with self._client.get_session() as session:
            try:
                obj = await session.get(UserSchema, user_id)
                if not obj:
                    return False
                await session.delete(obj)
                await session.flush()
                await session.commit()
                await self._logger.ainfo("User deleted", user_id=user_id)
            except Exception:
                await self._logger.aexception("Failed to delete user", user_id=user_id)
                raise

    @logfire.instrument("create_lesson")
    async def create_lesson(self, lesson: Lesson) -> Lesson:
        async with self._client.get_session() as session:
            try:
                obj = LessonSchema(**lesson.model_dump(exclude_none=True))
                session.add(obj)
                await session.flush()
                await session.commit()
                await session.refresh(obj)
                await self._logger.ainfo("Lesson created", lesson=lesson)
                return Lesson.model_validate(obj)
            except Exception:
                await self._logger.aexception("Failed to create lesson", lesson=lesson)
                raise

    @logfire.instrument("create_document")
    async def create_document(self, document: Document) -> Document:
        async with self._client.get_session() as session:
            try:
                obj = DocumentSchema(**document.model_dump(exclude_none=True))
                session.add(obj)
                await session.flush()
                await session.commit()
                await session.refresh(obj)
                await self._logger.ainfo("Document created", document=document)
                return Document.model_validate(obj)
            except Exception:
                await self._logger.aexception(
                    "Failed to create document", document=document
                )
                raise

    @logfire.instrument("create_result")
    async def create_result(self, result: Result) -> Result:
        async with self._client.get_session() as session:
            try:
                obj = ResultSchema(**result.model_dump(exclude_none=True))
                session.add(obj)
                await session.flush()
                await session.commit()
                await session.refresh(obj)
                await self._logger.ainfo("Result created", result=result)
                return Result.model_validate(obj)
            except Exception:
                await self._logger.aexception("Failed to create result", result=result)
                raise

    @logfire.instrument("get_lesson_by_id")
    async def get_lesson_by_id(self, lesson_id: int):
        async with self._client.get_session() as session:
            try:
                result = await session.get(LessonSchema, lesson_id)
                if not result:
                    return None
                return Lesson.model_validate(result)
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch lesson by id", lesson_id=lesson_id
                )
                raise

    @logfire.instrument("get_document_by_id")
    async def get_document_by_id(self, document_id: int):
        async with self._client.get_session() as session:
            try:
                result = await session.get(DocumentSchema, document_id)
                if not result:
                    return None
                return Document.model_validate(result)
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch document by id", document_id=document_id
                )
                raise

    @logfire.instrument("get_result_by_id")
    async def get_result_by_id(self, result_id: int):
        async with self._client.get_session() as session:
            try:
                result = await session.get(ResultSchema, result_id)
                if not result:
                    return None
                return Result.model_validate(result)
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch result by id", result_id=result_id
                )
                raise

    @logfire.instrument("update_result")
    async def update_result(self, result: Result) -> Result:
        async with self._client.get_session() as session:
            try:
                obj = ResultSchema(**result.model_dump(exclude_none=True))
                session.add(obj)
                await session.commit()
                await session.flush()
                await session.refresh(obj)
                await self._logger.ainfo("Result updated", result=result)
                return Result.model_validate(obj)
            except Exception:
                await self._logger.aexception("Failed to update result", result=result)
                raise

    @logfire.instrument("delete_result")
    async def delete_result(self, result_id: int):
        async with self._client.get_session() as session:
            try:
                obj = await session.get(ResultSchema, result_id)
                if not obj:
                    return False
                await session.delete(obj)
                await session.flush()
                await session.commit()
                await self._logger.ainfo("Result deleted", result_id=result_id)
            except Exception:
                await self._logger.aexception(
                    "Failed to delete result", result_id=result_id
                )
                raise

    @logfire.instrument("delete_document")
    async def delete_document(self, document_id: int):
        async with self._client.get_session() as session:
            try:
                obj = await session.get(DocumentSchema, document_id)
                if not obj:
                    return False
                await session.delete(obj)
                await session.flush()
                await session.commit()
                await self._logger.ainfo("Document deleted", document_id=document_id)
            except Exception:
                await self._logger.aexception(
                    "Failed to delete document", document_id=document_id
                )
                raise

    @logfire.instrument("delete_lesson")
    async def delete_lesson(self, lesson_id: int):
        async with self._client.get_session() as session:
            try:
                obj = await session.get(LessonSchema, lesson_id)
                if not obj:
                    return False
                await session.delete(obj)
                await session.flush()
                await session.commit()
                await self._logger.ainfo("Lesson deleted", lesson_id=lesson_id)
            except Exception:
                await self._logger.aexception(
                    "Failed to delete lesson", lesson_id=lesson_id
                )
                raise

    @logfire.instrument("update_lesson")
    async def update_lesson(self, lesson: Lesson) -> Lesson:
        async with self._client.get_session() as session:
            try:
                obj = LessonSchema(**lesson.model_dump(exclude_none=True))
                session.add(obj)
                await session.commit()
                await session.flush()
                await session.refresh(obj)
                await self._logger.ainfo("Lesson updated", lesson=lesson)
                return Lesson.model_validate(obj)
            except Exception:
                await self._logger.aexception("Failed to update lesson", lesson=lesson)
                raise

    @logfire.instrument("update_document")
    async def update_document(self, document: Document) -> Document:
        async with self._client.get_session() as session:
            try:
                obj = DocumentSchema(**document.model_dump(exclude_none=True))
                session.add(obj)
                await session.commit()
                await session.flush()
                await session.refresh(obj)
                await self._logger.ainfo("Document updated", document=document)
                return Document.model_validate(obj)
            except Exception:
                await self._logger.aexception(
                    "Failed to update document", document=document
                )
                raise

    @logfire.instrument
    async def get_lessons(self):
        async with self._client.get_session() as session:
            try:
                result = await session.execute(
                    select(LessonSchema).order_by(LessonSchema.createdAt.desc())
                )
                return [Lesson.model_validate(obj) for obj in result.scalars().all()]
            except Exception:
                await self._logger.aexception("Failed to fetch lessons")
                raise

    @logfire.instrument
    async def get_results_by_user_id(self, user_id: int) -> list[Result]:
        async with self._client.get_session() as session:
            try:
                result = await session.execute(
                    select(ResultSchema).where(ResultSchema.userId == user_id)
                )
                return [Result.model_validate(obj) for obj in result.scalars().all()]
            except Exception:
                await self._logger.aexception(
                    "Failed to fetch results by user id", user_id=user_id
                )
                raise
