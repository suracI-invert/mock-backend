import asyncio

from infra.gemini import get_gemini

from pydantic_ai.agent import Agent
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
)

agent = Agent(get_gemini())

message_history = []


def parse_history(history: list[ModelMessage]):
    print("=" * 50)
    for mm in history:
        print(mm)
        print("-" * 50)


def parse_history_format(history: list[ModelMessage]):
    new_history = []
    for mm in history:
        if mm.kind == "request":
            for part in mm.parts:
                if part.part_kind == "user-prompt":
                    new_history.append({"role": "user", "content": part.content})
        elif mm.kind == "response":
            for part in mm.parts:
                if part.part_kind == "text":
                    new_history.append({"role": "assistant", "content": part.content})
    import json

    return json.dumps(new_history, indent=4)


async def chat():
    global message_history
    is_running = True
    while is_running:
        user_input = input(">> ")
        if user_input == "$EXIT":
            is_running = False
        else:
            async with agent.run_stream(
                user_input, message_history=message_history
            ) as stream:
                async for resp in stream.stream_text(delta=True, debounce_by=None):
                    print(resp, end="")
                message_history = stream.all_messages()
    print(parse_history_format(message_history))


asyncio.run(chat())
