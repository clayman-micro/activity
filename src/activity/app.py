import socket
from uuid import uuid4

import pkg_resources
from aiohttp import web
from structlog.contextvars import bind_contextvars, clear_contextvars
from structlog.types import WrappedLogger

from activity.web import meta


@web.middleware
async def logging_middleware(request, handler):
    """Logging middleware.

    Args:
        request: Current request instance.
        handler: Handler for request.
    """
    clear_contextvars()

    context_vars = {
        "request_id": request.headers.get("X-Request-ID", str(uuid4().hex)),
        "request_method": request.method,
    }

    if "X-Correlation-ID" in request.headers:
        context_vars["correlation_id"] = request.headers["X-Correlation-ID"]

    bind_contextvars(**context_vars)

    resp = await handler(request)

    bind_contextvars(response_status=resp.status)
    return resp


def init(app_name: str, logger: WrappedLogger) -> web.Application:
    """Create application instance.

    Args:
        app_name: Application name.
        logger: Logger instance.

    Return:
        New application instance.
    """
    app = web.Application(logger=logger.bind(context="app"), middlewares=[logging_middleware])

    app["app_name"] = app_name
    app["hostname"] = socket.gethostname()
    app["distribution"] = pkg_resources.get_distribution(app_name)

    app.router.add_get("/-/meta", handler=meta.index, name="meta", allow_head=False)
    app.router.add_get("/-/health", handler=meta.health, name="health", allow_head=False)

    return app
