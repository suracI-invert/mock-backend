from dataclasses import dataclass

import logfire.propagate
from starlette.types import Scope, Receive, Send, ASGIApp

from structlog.stdlib import BoundLogger

from log import get_logger


import logfire


@dataclass
class TraceMiddleware:
    app: ASGIApp
    logger: BoundLogger = get_logger("middleware.trace")
    header_name: str = "X-Request-Process-Time"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Load request ID from headers if present. Generate one otherwise.
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return
        path = scope.get("path", "")
        method = scope.get("method", "")

        with logfire.span(f"Request to {method} {path}"):
            trace_context = logfire.propagate.get_context()
            await self.logger.ainfo(
                "Trace context generated", trace_context=trace_context
            )
            scope["trace_context"] = trace_context
            await self.app(scope, receive, send)
        return
