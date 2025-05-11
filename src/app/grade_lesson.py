from datetime import datetime
from typing import Literal
from pydantic import BaseModel
from fastapi import HTTPException

from domain.agents.listening_grader import (
    grade_listening_lesson,
    ListeningExerciseResult,
)
from domain.agents.reading_grader import (
    grade_reading_lesson,
    ReadingExerciseResult,
)
from infra.data.crud import DataBackend
from infra.data.models import Result

from .utils import convert_level


class Exercise(BaseModel):
    index: int
    question: str
    answers: list[str]
    student_answer: int


class ExerciseWithKey(BaseModel):
    index: int
    question: str
    answers: list[str]
    student_answer: int
    correct_answer: int


class Grade(BaseModel):
    exercises: list[ExerciseWithKey]
    score: int
    max_score: int
    overall_comment: str
    detail_comment: str
    suggestions: str


async def grade_lesson(
    lesson_id: int,
    user_id: int,
    start_date: datetime,
    transcript: str,
    exercises: list[Exercise],
    level: int,
    lesson_type: Literal["listening", "reading", "speaking"],
    db: DataBackend,
):
    lesson = await db.get_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    questions = lesson.content.get("questions")

    assert questions
    new_exercises = [
        ExerciseWithKey(
            index=e.index,
            question=e.question,
            answers=e.answers,
            student_answer=e.student_answer,
            correct_answer=questions[e.index]["correct_answer"],
        )
        for e in exercises
    ]
    score, max_score = scorer(new_exercises)
    match lesson_type:
        case "listening":
            result = await grade_listening_lesson(
                transcript,
                [
                    ListeningExerciseResult(
                        question=e.question,
                        student_answer=e.answers[e.student_answer],
                        correct_answer=e.answers[e.correct_answer],
                    )
                    for e in new_exercises
                ],
                convert_level(level),
            )
        case "reading":
            result = await grade_reading_lesson(
                transcript,
                [
                    ReadingExerciseResult(
                        question=e.question,
                        student_answer=e.answers[e.student_answer],
                        correct_answer=e.answers[e.correct_answer],
                    )
                    for e in new_exercises
                ],
                convert_level(level),
            )
        case "speaking":
            raise NotImplementedError

    grade = Grade(
        exercises=new_exercises,
        score=score,
        max_score=max_score,
        overall_comment=result.overall_comment,
        detail_comment=result.detail_comment,
        suggestions=result.suggestions,
    )

    _ = await db.create_result(
        Result(
            score=grade.score,
            maxScore=grade.max_score,
            comment=grade.overall_comment,
            detail={
                "overall_comment": grade.overall_comment,
                "detail_comment": grade.detail_comment,
                "suggestions": grade.suggestions,
            },
            startedAt=start_date,
            lessonId=lesson_id,
            userId=user_id,
        )
    )

    return grade


def scorer(exercises: list[ExerciseWithKey]):
    no_correct = 0
    for exercise in exercises:
        if exercise.student_answer == exercise.correct_answer:
            no_correct += 1

    return no_correct, len(exercises)
