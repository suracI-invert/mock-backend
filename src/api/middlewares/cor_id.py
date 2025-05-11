from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass
from dataclasses import field
import uuid

from starlette.datastructures import MutableHeaders
from starlette.types import Scope, Receive, Send, ASGIApp, Message

import structlog
from structlog.stdlib import BoundLogger

from log import get_logger


correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)


def uuid4_generator() -> str:
    return uuid.uuid4().hex


def uuid4_validator(uid: str) -> bool:
    try:
        return uuid.UUID(uid).version == 4
    except ValueError:
        return False


@dataclass
class CorrelationIDMiddleware:
    app: ASGIApp
    logger: BoundLogger = get_logger("middleware.id")
    header_name: str = "X-Request-ID"
    uid_generator: Callable[..., str] = field(default=uuid4_generator)
    uid_validator: Callable[[str], bool] = field(default=uuid4_validator)
    uid_transformer: Callable[[str], str] = field(default=lambda x: x)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Load request ID from headers if present. Generate one otherwise.
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        # Try to load request ID from the request headers
        headers = MutableHeaders(scope=scope)
        header_value = headers.get(self.header_name.lower())

        validation_failed = False
        if not header_value:
            # Generate request ID if none was found
            id_value = self.uid_generator()
        elif self.uid_validator and not self.uid_validator(header_value):
            # Also generate a request ID if one was found, but it was deemed invalid
            validation_failed = True
            id_value = self.uid_generator()
        else:
            # Otherwise, use the found request ID
            id_value = header_value

        # Clean/change the ID if needed
        if self.uid_transformer:
            id_value = self.uid_transformer(id_value)

        if validation_failed is True:
            await self.logger.awarning(
                "Request Header ID validation failed, generate new request ID",
                request_id=id_value,
            )

        # Update the request headers if needed
        if id_value != header_value:
            headers[self.header_name] = id_value

        correlation_id.set(id_value)

        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=id_value)

        async def handle_outgoing_request(message: Message) -> None:
            corr_id = correlation_id.get()
            if message["type"] == "http.response.start" and corr_id:
                headers = MutableHeaders(scope=message)
                headers.append(self.header_name, corr_id)

            await send(message)

        await self.app(scope, receive, handle_outgoing_request)
        return
