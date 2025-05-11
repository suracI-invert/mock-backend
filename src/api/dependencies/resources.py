from typing import Annotated

from fastapi import Depends

from infra.db.postgre import PostgresClient
from infra.data.crud import DataBackend

from settings import Settings, get_settings


async def get_postgres_client(settings: Annotated[Settings, Depends(get_settings)]):
    return await PostgresClient.init(settings.postgre)


async def get_data_backend(
    client: Annotated[PostgresClient, Depends(get_postgres_client)],
) -> DataBackend:
    return DataBackend(client)
