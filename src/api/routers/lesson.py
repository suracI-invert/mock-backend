from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException


from app.upload_lesson import (
    upload_listening_lesson,
    upload_reading_lesson,
    upload_speaking_lesson,
    ListeningLesson,
    ReadingLesson,
    SpeakingLesson,
    Question,
)

from ..models.share import LessonType

from app.generate_lesson import generate_ai_lesson, GenerateLesson as GenerateAILesson

from infra.data.crud import DataBackend

from ..models.lesson import (
    GenerateLesson,
    GeneratedLesson,
    ListeningContent,
    MultipleChoicesQuestion,
    ReadingContent,
    SpeakingContent,
    UploadLesson,
    LessonReturned,
)
from ..dependencies.resources import get_data_backend

router = APIRouter(prefix="/lesson/v1", tags=["lesson"])


@router.get("/list")
async def list_lessons(
    db: Annotated[DataBackend, Depends(get_data_backend)],
) -> list[LessonReturned]:
    results = await db.get_lessons()
    lessons = []
    for result in results:
        if result.authorId:
            author = await db.get_user_by_id(result.authorId)
        else:
            author = None
        lesson = result.model_dump(exclude={"authorId"})
        lesson["author"] = (
            {
                "id": author.id,
                "name": author.name,
                "email": author.email,
                "avatarUrl": author.avatarUrl,
                "is_logged_in": author.is_logged_in,
                "createdAt": author.createdAt,
                "updatedAt": author.updatedAt,
            }
            if author
            else {}
        )
        lessons.append(lesson)
    return [LessonReturned.model_validate(lesson) for lesson in lessons]


@router.get("/{lesson_id}")
async def get_lesson_by_id(
    lesson_id: int,
    db: Annotated[DataBackend, Depends(get_data_backend)],
) -> LessonReturned:
    result = await db.get_lesson_by_id(lesson_id)
    if not result:
        raise HTTPException(404, "Lesson not found")
    if result.authorId:
        author = await db.get_user_by_id(result.authorId)
    else:
        author = None
    lesson = result.model_dump(exclude={"authorId"})
    lesson["author"] = {"id": author.id, "name": author.name} if author else {}
    return LessonReturned.model_validate(lesson)


@router.post("/upload")
async def upload_lesson(
    req: UploadLesson,
    db: Annotated[DataBackend, Depends(get_data_backend)],
):
    lesson = req.data
    match lesson.type:
        case LessonType.SPEAKING.value:
            assert isinstance(lesson.content, SpeakingContent)
            ret = await upload_speaking_lesson(
                SpeakingLesson(
                    name=lesson.name,
                    description=lesson.description,
                    type=lesson.type,
                    level=lesson.level,
                    authorId=lesson.authorId,
                    topic=lesson.content.topic,
                    main_question=lesson.content.main_question,
                    guidelines=lesson.content.guidelines,
                ),
                db,
            )
        case LessonType.LISTENING.value:
            assert isinstance(lesson.content, ListeningContent)
            ret = await upload_listening_lesson(
                ListeningLesson(
                    name=lesson.name,
                    description=lesson.description,
                    transcript=lesson.content.transcript,
                    audio_url=lesson.content.audio_url,
                    questions=[
                        Question(
                            index=q.index,
                            answers=q.answers,
                            correct_answer=q.correct_answer,
                            question=q.text,
                        )
                        for q in lesson.content.questions
                    ],
                    type=lesson.type,
                    level=lesson.level,
                    authorId=lesson.authorId,
                ),
                db,
            )
        case LessonType.READING.value:
            assert isinstance(lesson.content, ReadingContent)
            ret = await upload_reading_lesson(
                ReadingLesson(
                    name=lesson.name,
                    description=lesson.description,
                    text=lesson.content.text,
                    questions=[
                        Question(
                            index=q.index,
                            answers=q.answers,
                            correct_answer=q.correct_answer,
                            question=q.text,
                        )
                        for q in lesson.content.questions
                    ],
                    type=lesson.type,
                    level=lesson.level,
                    authorId=lesson.authorId,
                ),
                db,
            )
    return {"id": ret[0], "lesson": ret[1]}


@router.post("/generate")
async def generate_lesson(req: GenerateLesson):
    match req.type.value:
        case "speaking":
            result = await generate_ai_lesson(
                GenerateAILesson(
                    text_source=req.text,
                    level=req.level,
                ),
                req.type.value,
            )
            return GeneratedLesson(
                type=req.type,
                level=req.level,
                content=SpeakingContent(
                    topic=req.text,
                    main_question=result.main_question,
                    guidelines=result.guidelines,
                ),
            )
        case "listening":
            result = await generate_ai_lesson(
                GenerateAILesson(
                    text_source=req.text,
                    level=req.level,
                ),
                req.type.value,
            )
            return GeneratedLesson(
                type=req.type,
                level=req.level,
                content=ListeningContent(
                    transcript=req.text,
                    audio_url="",
                    questions=[
                        MultipleChoicesQuestion(
                            index=i,
                            text=q.question,
                            answers=q.answer,
                            correct_answer=q.correct_answer,
                        )
                        for i, q in enumerate(result.questions)
                    ],
                ),
            )
        case "reading":
            result = await generate_ai_lesson(
                GenerateAILesson(
                    text_source=req.text,
                    level=req.level,
                ),
                req.type.value,
            )
            return GeneratedLesson(
                type=req.type,
                level=req.level,
                content=ReadingContent(
                    text=req.text,
                    questions=[
                        MultipleChoicesQuestion(
                            index=i,
                            text=q.question,
                            answers=q.answer,
                            correct_answer=q.correct_answer,
                        )
                        for i, q in enumerate(result.questions)
                    ],
                ),
            )
