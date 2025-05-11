from datetime import datetime
from typing import Annotated, Any, Literal
from pydantic import BaseModel, BeforeValidator

from .share import Level, LessonType, validate_datetime


class Question(BaseModel):
    index: int
    question: str
    answers: list[str]
    student_answer: int


class GradeExercise(BaseModel):
    lesson_id: int
    user_id: int
    # start_date: Annotated[datetime | str, BeforeValidator(validate_datetime)]
    # start_date: datetime = datetime.now()
    transcript: str
    level: Level
    questions: list[Question]
    lesson_type: LessonType


class SpeakingRequest(BaseModel):
    session_id: str
    part: Literal["p1", "p2", "p3"]
    content: str
    topic: str
    main_question: str
    guidelines: list[str]
    level: Level


class SpeakingResponse(BaseModel):
    response: str
    is_end: bool
    history: dict[str, list[dict[str, str]]]
