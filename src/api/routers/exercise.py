from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies.resources import get_data_backend
from ..models.exercise import GradeExercise, SpeakingRequest, SpeakingResponse
from app.chat import speak
from app.grade_lesson import grade_lesson, Exercise
from infra.data.crud import DataBackend
from domain.agents.chat import SpeakingPart

router = APIRouter(prefix="/exercise/v1", tags=["exercise"])


@router.post("/grade")
async def grade_exercise(
    exercise: GradeExercise,
    data_backend: Annotated[DataBackend, Depends(get_data_backend)],
):
    grade = await grade_lesson(
        exercise.lesson_id,
        exercise.user_id,
        datetime.now(),
        exercise.transcript,
        [
            Exercise(
                index=q.index,
                question=q.question,
                answers=q.answers,
                student_answer=q.student_answer,
            )
            for q in exercise.questions
        ],
        exercise.level,
        exercise.lesson_type.value,
        data_backend,
    )
    return grade


@router.post("/speaking")
async def speaking(req: SpeakingRequest) -> SpeakingResponse:
    r = await speak(
        user_prompt=req.content,
        level=req.level,
        session_id=req.session_id,
        topic=req.topic,
        main_question=req.main_question,
        guidelines=req.guidelines,
        part=SpeakingPart(req.part),
        is_end=False,
    )
    return SpeakingResponse(response=r.response, is_end=r.is_end, history=r.history)


@router.get("/stat/{user_id}")
async def get_user_stat(
    user_id: int, data_backend: Annotated[DataBackend, Depends(get_data_backend)]
):
    return None
