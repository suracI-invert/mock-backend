from typing import Protocol
from dataclasses import dataclass, field
from collections import defaultdict

from pydantic_ai.messages import ModelMessage


class ConversationStorage(Protocol):
    async def add_message(self, uid: str, messages: list[ModelMessage]) -> None: ...

    async def get_messages(self, uid: str) -> list[ModelMessage]: ...


@dataclass
class InMemoryStorage(ConversationStorage):
    _dict: defaultdict[str, list[ModelMessage]] = field(
        default_factory=lambda: defaultdict(list)
    )

    async def add_message(self, uid: str, messages: list[ModelMessage]) -> None:
        self._dict[uid].extend(messages)

    async def get_messages(self, uid: str) -> list[ModelMessage]:
        return self._dict[uid]
