from pydantic_ai import Agent
from pydantic import BaseModel

from infra.gemini import get_gemini

SYSTEM_PROMPT = """You are an English Instructor who is a expert in teaching English.
Your job is to create a reading excercise for students from given text source.
Given the level of A1, A2, B1, B2, C1 and C2, create an appropriate reading excercise.

The exercise should consist of 6 questions and each question should be of the multiple choices format:
{{
    "question": "question",
    "answer": ["answer1", "answer2", "answer3", "answer4"],
    "correct_answer": index of correct answer
}}
"""

USER_PROMPT = """Text source: {text_source}
Level: {level}
"""


class ReadingQuestion(BaseModel):
    question: str
    answer: list[str]
    correct_answer: int


class ReadingExercise(BaseModel):
    questions: list[ReadingQuestion]


async def generate_reading_lesson(text: str, level: str):
    agent = Agent(
        get_gemini(), system_prompt=SYSTEM_PROMPT, output_type=ReadingExercise
    )

    return (await agent.run(USER_PROMPT.format(text_source=text, level=level))).output
