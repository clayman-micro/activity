import socket

import pkg_resources
from aiohttp import web
from structlog.types import WrappedLogger

from activity.logging import setup as setup_logging
from activity.metrics import setup as setup_metrics
from activity.web import meta


def init(app_name: str, logger: WrappedLogger) -> web.Application:
    """Create application instance.

    Args:
        app_name: Application name.
        logger: Logger instance.

    Return:
        New application instance.
    """
    app = web.Application()

    app["app_name"] = app_name
    app["hostname"] = socket.gethostname()
    app["distribution"] = pkg_resources.get_distribution(app_name)

    setup_logging(app, logger=logger)
    setup_metrics(app)

    app.router.add_get("/-/meta", handler=meta.index, name="meta", allow_head=False)
    app.router.add_get("/-/health", handler=meta.health, name="health", allow_head=False)

    return app
