from dataclasses import dataclass

import logfire.propagate
from starlette.types import Scope, Receive, Send, ASGIApp

from structlog.stdlib import BoundLogger

from log import get_logger


import logfire


@dataclass
class ConnectionCounterMiddleware:
    app: ASGIApp
    logger: BoundLogger = get_logger("middleware.connection_counter")
    _total_connections = logfire.metric_counter(
        "total_connections",
        unit="1",
        description="Total Connections connected throughout the lifetime of the server",
    )
    _concurrent_connections = logfire.metric_up_down_counter(
        "concurrent_connections",
        unit="1",
        description="Concurrent Connections connected",
    )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Load request ID from headers if present. Generate one otherwise.
        """
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        self._total_connections.add(1)
        self._concurrent_connections.add(1)
        try:
            await self.app(scope, receive, send)
        except Exception:
            raise
        finally:
            self._concurrent_connections.add(-1)
        return
