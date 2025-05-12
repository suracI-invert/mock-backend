from typing import Annotated

from fastapi import Depends, Request
from pydantic_ai.models import Model

from domain.assistants.conversation_storage import ConversationStorage
from infra.db.postgre import PostgresClient
from infra.data.crud import DataBackend
from infra.gemini import get_gemini

from settings import Settings, get_settings


async def get_postgres_client(settings: Annotated[Settings, Depends(get_settings)]):
    return await PostgresClient.init(settings.postgre)


async def get_data_backend(
    client: Annotated[PostgresClient, Depends(get_postgres_client)],
) -> DataBackend:
    return DataBackend(client)


async def get_pydantic_ai_model(req: Request) -> Model:
    return get_gemini()


async def get_conversation_storage(req: Request) -> ConversationStorage:
    return req.app.state.conversation_storage
