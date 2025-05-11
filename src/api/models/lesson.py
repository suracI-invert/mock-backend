from typing import Any, Literal
from pydantic import BaseModel, Field

from .share import Level, LessonType


class SpeakingContent(BaseModel):
    topic: str
    main_question: str
    guidelines: list[str]


class MultipleChoicesQuestion(BaseModel):
    index: int
    text: str
    answers: list[str]
    correct_answer: int


class ListeningContent(BaseModel):
    transcript: str
    audio_url: str
    questions: list[MultipleChoicesQuestion]


class ReadingContent(BaseModel):
    text: str
    questions: list[MultipleChoicesQuestion]


class UploadListeningLesson(BaseModel):
    name: str
    authorId: int
    type: Literal["listening"]
    level: Level
    description: str
    content: ListeningContent


class UploadSpeakingLesson(BaseModel):
    name: str
    authorId: int
    type: Literal["speaking"]
    level: Level
    description: str
    content: SpeakingContent


class UploadReadingLesson(BaseModel):
    name: str
    authorId: int
    type: Literal["reading"]
    level: Level
    description: str
    content: ReadingContent


class UploadLesson(BaseModel):
    data: UploadSpeakingLesson | UploadListeningLesson | UploadReadingLesson = Field(
        discriminator="type"
    )


class Author(BaseModel):
    id: int
    name: str


class LessonReturned(BaseModel):
    id: int
    name: str
    description: str
    type: LessonType
    level: Level
    author: Author | dict = {}
    content: dict[str, Any]


class GenerateLesson(BaseModel):
    text: str
    type: LessonType
    level: Level


class GeneratedLesson(BaseModel):
    type: LessonType
    level: Level
    content: SpeakingContent | ListeningContent | ReadingContent
