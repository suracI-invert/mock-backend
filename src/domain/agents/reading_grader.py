from pydantic_ai import Agent
from pydantic import BaseModel, Field

from infra.gemini import get_gemini

SYSTEM_PROMPT = """You are an English Instructor who is a expert in teaching English.
Your job is to grade a reading excercise for students.
Given the level of A1, A2, B1, B2, C1 and C2 of the exercise, grade the exercise appropriately.

You should get into details on what is wrong with the student's answer, reason and show reference/hightlight the text that show they are wrong and give suggestions on how to improve before give out overall comment on their performance.
You will be given the reading text, questions, the student's answers and the correct answers.
"""

USER_PROMPT = """Text : {text}
Exercise: 
{exercise}
Level: {level}
"""


class ReadingExerciseGrade(BaseModel):
    overall_comment: str = Field(
        description="Overall comment about the student performance"
    )
    detail_comment: str = Field(
        description="Detailed comment about each answer of the student"
    )
    suggestions: str = Field(
        description="Suggestions on how to improve student performance"
    )


class ReadingExerciseResult(BaseModel):
    question: str
    student_answer: str
    correct_answer: str


def parse_reading_exercise(exercises: list[ReadingExerciseResult]) -> str:
    return "\n".join(
        [
            f"\tQuestion: {exercise.question}\nStudent Answer: {exercise.student_answer}\nCorrect Answer: {exercise.correct_answer}"
            for exercise in exercises
        ]
    )


async def grade_reading_lesson(
    text: str, exercises: list[ReadingExerciseResult], level: str
):
    agent = Agent(
        get_gemini(), system_prompt=SYSTEM_PROMPT, output_type=ReadingExerciseGrade
    )

    return (
        await agent.run(
            USER_PROMPT.format(
                text=text,
                exercise=parse_reading_exercise(exercises),
                level=level,
            )
        )
    ).output
