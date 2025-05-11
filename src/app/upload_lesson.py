from pydantic import BaseModel

from infra.data.crud import DataBackend
from infra.data.models import Lesson, Document


class LessonBase(BaseModel):
    name: str
    description: str
    type: str
    level: int
    authorId: int


class Question(BaseModel):
    index: int
    question: str
    answers: list[str]
    correct_answer: int


class ListeningLesson(LessonBase):
    transcript: str
    audio_url: str
    questions: list[Question]


class ReadingLesson(LessonBase):
    text: str
    questions: list[Question]


class SpeakingLesson(LessonBase):
    topic: str
    main_question: str
    guidelines: list[str]


async def upload_listening_lesson(
    lesson: ListeningLesson,
    data_backend: DataBackend,
):
    new_lesson = Lesson(
        name=lesson.name,
        description=lesson.description,
        type=lesson.type,
        level=lesson.level,
        content={
            "transcript": lesson.transcript,
            "audio_url": lesson.audio_url,
            "questions": [q.model_dump() for q in lesson.questions],
        },
        authorId=lesson.authorId,
    )
    new_lesson = await data_backend.create_lesson(new_lesson)
    new_document = Document(url=lesson.audio_url, lessonId=new_lesson.id)
    new_document = await data_backend.create_document(new_document)

    assert new_lesson.id
    assert new_lesson.authorId

    return new_lesson.id, ListeningLesson(
        name=new_lesson.name,
        description=new_lesson.description,
        type=new_lesson.type,
        level=new_lesson.level,
        authorId=new_lesson.authorId,
        transcript=new_lesson.content["transcript"],
        audio_url=new_document.url,
        questions=new_lesson.content["questions"],
    )


async def upload_reading_lesson(lesson: ReadingLesson, data_backend: DataBackend):
    new_lesson = Lesson(
        name=lesson.name,
        description=lesson.description,
        type=lesson.type,
        level=lesson.level,
        content={
            "text": lesson.text,
            "questions": [q.model_dump() for q in lesson.questions],
        },
        authorId=lesson.authorId,
    )
    new_lesson = await data_backend.create_lesson(new_lesson)

    assert new_lesson.id
    assert new_lesson.authorId

    return new_lesson.id, ReadingLesson(
        name=new_lesson.name,
        description=new_lesson.description,
        type=new_lesson.type,
        level=new_lesson.level,
        authorId=new_lesson.authorId,
        text=new_lesson.content["text"],
        questions=new_lesson.content["questions"],
    )


async def upload_speaking_lesson(lesson: SpeakingLesson, data_backend: DataBackend):
    new_lesson = Lesson(
        name=lesson.name,
        description=lesson.description,
        type=lesson.type,
        level=lesson.level,
        content={
            "topic": lesson.topic,
            "main_question": lesson.main_question,
            "guidelines": lesson.guidelines,
        },
        authorId=lesson.authorId,
    )
    new_lesson = await data_backend.create_lesson(new_lesson)

    assert new_lesson.id
    assert new_lesson.authorId

    return new_lesson.id, SpeakingLesson(
        name=new_lesson.name,
        description=new_lesson.description,
        type=new_lesson.type,
        level=new_lesson.level,
        authorId=new_lesson.authorId,
        topic=new_lesson.content["topic"],
        main_question=new_lesson.content["main_question"],
        guidelines=new_lesson.content["guidelines"],
    )
