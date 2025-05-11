from typing import overload, Literal
from pydantic import BaseModel

from domain.agents.create_listening import ListeningExercise, generate_listening_lesson
from domain.agents.create_reading import ReadingExercise, generate_reading_lesson
from domain.agents.create_speaking import (
    SpeakingPart2Exercise,
    generate_speaking_p2_lesson,
)

from .utils import convert_level


class GenerateLesson(BaseModel):
    text_source: str
    level: int


class GeneratedReadingQuestion(BaseModel):
    question: str
    answer: list[str]
    correct_answer: int


class GeneratedListeningQuestion(BaseModel):
    question: str
    answer: list[str]
    correct_answer: int


class GeneratedSpeakingPart2Question(BaseModel):
    main_question: str
    guidelines: list[str]


@overload
async def generate_ai_lesson(
    req: GenerateLesson, lesson_type: Literal["reading"]
) -> ReadingExercise: ...


@overload
async def generate_ai_lesson(
    req: GenerateLesson, lesson_type: Literal["listening"]
) -> ListeningExercise: ...


@overload
async def generate_ai_lesson(
    req: GenerateLesson, lesson_type: Literal["speaking"]
) -> SpeakingPart2Exercise: ...


async def generate_ai_lesson(
    req: GenerateLesson, lesson_type: Literal["reading", "listening", "speaking"]
) -> ReadingExercise | ListeningExercise | SpeakingPart2Exercise:
    match lesson_type:
        case "reading":
            return await generate_reading_lesson(
                req.text_source, convert_level(req.level)
            )
        case "listening":
            return await generate_listening_lesson(
                req.text_source, convert_level(req.level)
            )
        case "speaking":
            return await generate_speaking_p2_lesson(
                req.text_source, convert_level(req.level)
            )
        case _:
            raise ValueError(f"Invalid type {lesson_type}")
