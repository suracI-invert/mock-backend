from pydantic_ai import Agent
from pydantic import BaseModel, Field

from infra.gemini import get_gemini

SYSTEM_PROMPT_SPEAKING_2 = """You are an English Instructor who is a expert in teaching English.
Your job is to create a speaking excercise for students from given text source.
Given the level of A1, A2, B1, B2, C1 and C2, create an appropriate speaking excercise.

This is in format of IELTS Speaking Part 2, which focuses on student talking about a particular question.
Given the topic, your job is to create a question card which consists of:
- Main question
- Guidelines/Suggestions on how student can answer that main question (You should say...)

For examples:
Topic: Experience
Main question: Describe an occasion when you had to wait a long time for someone or something to arrive.
Guidelines (You should say):
    - Who or what you were waiting for?
    - How long you had to wait?
    - Why you had to wait a long time and explain how you felt about waiting a long time.

"""

USER_PROMPT_SPEAKING_2 = """Topic: {topic}
Level: {level}
"""


class SpeakingPartQuestion(BaseModel):
    question: str
    answer: list[str]
    correct_answer: int


class SpeakingPart2Exercise(BaseModel):
    main_question: str = Field(description="Main question of the question card")
    guidelines: list[str] = Field(
        description="Guidelines on how student should answer the main question"
    )


async def generate_speaking_p2_lesson(topic: str, level: str):
    agent = Agent(
        get_gemini(),
        system_prompt=SYSTEM_PROMPT_SPEAKING_2,
        output_type=SpeakingPart2Exercise,
    )

    return (
        await agent.run(USER_PROMPT_SPEAKING_2.format(topic=topic, level=level))
    ).output


# async def generate_speaking_p1_lesson()
