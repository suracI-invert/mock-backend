from collections.abc import AsyncGenerator
from typing import Any, Literal, overload
from pydantic import BaseModel
from pydantic_ai.models import Model

from domain.agents.chat import (
    get_conversation_history,
    save_conversation_history,
    SpeakingPart,
    unload_conversation_history,
)

from domain.agents.speaking import speaking_p1, speaking_p2, speaking_p3
from domain.assistants.agent import Assistant
from domain.assistants.models import Context
from domain.assistants.conversation_storage import ConversationStorage
from domain.assistants.runners import bind_context
from .utils import convert_level


class ChatResponse(BaseModel):
    response: str
    is_end: bool
    history: dict[str, list[dict[str, str]]]


async def speak(
    user_prompt: str,
    level: int,
    session_id: str,
    topic: str,
    main_question: str,
    guidelines: list[str],
    part: SpeakingPart,
    is_end: bool,
):
    match part:
        case SpeakingPart.P1:
            response, history = await speaking_p1(
                user_prompt,
                convert_level(level),
                get_conversation_history(session_id, part),
            )
            save_conversation_history(user_prompt, part, history)
            return ChatResponse(
                response=response.response,
                is_end=response.end,
                history=unload_conversation_history(session_id),
            )
        case SpeakingPart.P2:
            response, history = await speaking_p2(topic, main_question, guidelines)
            save_conversation_history(user_prompt, part, history)
            return ChatResponse(
                response=response.response,
                is_end=response.end,
                history=unload_conversation_history(session_id),
            )
        case SpeakingPart.P3:
            response, history = await speaking_p3(
                topic,
                main_question,
                user_prompt,
                user_prompt,
                convert_level(level),
                get_conversation_history(session_id, part),
            )
            save_conversation_history(user_prompt, part, history)
            cr = ChatResponse(
                response=response.response,
                is_end=response.end,
                history=unload_conversation_history(session_id),
            )
            # if response.end:
            #     delete_conversation_history(session_id)
            return cr


@overload
async def chat(
    message: str,
    context: Context,
    model: Model,
    conversation_storage: ConversationStorage,
    stream: Literal[False],
) -> str: ...


@overload
async def chat(
    message: str,
    context: Context,
    model: Model,
    conversation_storage: ConversationStorage,
    stream: Literal[True],
) -> AsyncGenerator[str, Any]: ...


async def chat(
    message: str,
    context: Context,
    model: Model,
    conversation_storage: ConversationStorage,
    stream: Literal[True, False] = False,
) -> AsyncGenerator[str, Any] | str:

    assistant = Assistant(
        storage=conversation_storage,
        context=context,
        model=model,
        system_prompt_runners=(bind_context,),
    )
    if stream:
        return assistant.chat_stream(message)
    else:
        return await assistant.chat(message)
