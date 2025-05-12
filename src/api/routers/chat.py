from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic_ai.models import Model

from app.chat import chat
from domain.assistants.models import Context
from domain.assistants.conversation_storage import ConversationStorage

from ..models.chat import ChatRequest, ChatResponse
from ..dependencies.resources import get_pydantic_ai_model, get_conversation_storage

router = APIRouter(prefix="/chat/v1", tags=["chat"])


@router.post("/")
async def chat_conversation(
    req: ChatRequest,
    model: Annotated[Model, Depends(get_pydantic_ai_model)],
    conversation_storage: Annotated[
        ConversationStorage, Depends(get_conversation_storage)
    ],
) -> ChatResponse:
    ret = await chat(
        message=req.message,
        context=Context(
            user_name=req.user, session_id=req.conversation_id, lang=req.lang
        ),
        model=model,
        conversation_storage=conversation_storage,
        stream=False,
    )

    return ChatResponse(content=ret)


@router.post("/stream")
async def chat_conversation_stream(
    req: ChatRequest,
    model: Annotated[Model, Depends(get_pydantic_ai_model)],
    conversation_storage: Annotated[
        ConversationStorage, Depends(get_conversation_storage)
    ],
):
    stream = await chat(
        message=req.message,
        context=Context(
            user_name=req.user, session_id=req.conversation_id, lang=req.lang
        ),
        model=model,
        conversation_storage=conversation_storage,
        stream=True,
    )

    return StreamingResponse(stream)


# @router.post("/")
