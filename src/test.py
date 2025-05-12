import asyncio

from infra.gemini import get_gemini
from domain.assistants.promts import SYSTEM_PROMPT

from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    UserPromptPart,
)


agent = Agent(
    get_gemini(),
    system_prompt="You are a helpful AI Assistant",
    deps_type=str,
)


@agent.system_prompt(dynamic=True)
async def deps(ctx: RunContext[str]) -> str:
    return f"The user's name is {ctx.deps}"


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
                user_input, message_history=message_history, deps="John"
            ) as stream:
                async for resp in stream.stream_text(delta=True, debounce_by=None):
                    print(resp, end="")
                # print(stream.new_messages())
                message_history = stream.all_messages()
    print(parse_history(message_history))


asyncio.run(chat())
